import os
import re
import requests
import subprocess

from config import GITHUB_USERNAME, GITHUB_TOKEN, BACKUP_DIR

# GitHub API URL for the user's gists
API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/gists"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Regex for GitHub image URLs in Markdown
img_regex = re.compile(r'(!\[.*?\]\()(https://(?:user-images\.githubusercontent\.com|github-production-user-asset-[^\s)]+)[^\s)]*)(\))')

os.makedirs(BACKUP_DIR, exist_ok=True)

def fetch_gists():
    """Fetch all gists from the GitHub API (including pagination)."""
    gists = []
    page = 1
    while True:
        response = requests.get(f"{API_URL}?page={page}&per_page=100", headers=headers)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen der API: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        gists.extend(data)
        page += 1
    return gists

def process_markdown_file(file_path, images_dir):
    """Scan a Markdown file, download images, and update image links."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = img_regex.findall(content)
    if not matches:
        return

    new_content = content
    for prefix, url, suffix in matches:
        # Extract a clean filename
        img_name = url.split("/")[-1].split("?")[0]
        local_img_path = os.path.join(images_dir, img_name)

        # Download the image if it does not already exist
        if not os.path.exists(local_img_path):
            try:
                print(f"  -> Downloading image: {img_name}")
                img_data = requests.get(url).content
                with open(local_img_path, "wb") as img_file:
                    img_file.write(img_data)
            except Exception as e:
                print(f"  [!] Error downloading image {url}: {e}")
                continue

        # Calculate the relative path for the Markdown file (pointing to the local 'images' folder)
        # Since the 'images' folder is directly inside the gist folder, 'images/name.png' is sufficient
        rel_path = f"images/{img_name}"
        old_link = f"{prefix}{url}{suffix}"
        new_link = f"{prefix}{rel_path}{suffix}"
        new_content = new_content.replace(old_link, new_link)

    # Update the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  -> Links in {os.path.basename(file_path)} updated successfully.")

def main():
    print("Starting gist backup process...")
    gists = fetch_gists()
    print(f"{len(gists)} gists found. Starting download via Git...")

    for gist in gists:
        gist_id = gist["id"]
        # Use the description as the folder name if available, otherwise use the ID
        description = gist["description"] or "Unnamed_Gist"
        # Clean folder names by removing invalid characters
        safe_desc = re.sub(r'[^\w\-_.]', '_', description)[:50]
        gist_folder_name = f"{safe_desc}_{gist_id}"
        gist_path = os.path.join(BACKUP_DIR, gist_folder_name)

        # 1. Clone or update the gist via Git
        if os.path.exists(gist_path):
            print(f"\nUpdating: {gist_folder_name}")
            subprocess.run(["git", "-C", gist_path, "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"\nCloning: {gist_folder_name}")
            # Use the token in the URL to allow cloning private gists as well
            clone_url = gist["git_pull_url"].replace("https://", f"https://{GITHUB_TOKEN}@")
            subprocess.run(["git", "clone", clone_url, gist_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Create the images directory within the gist
        images_dir = os.path.join(gist_path, "images")
        os.makedirs(images_dir, exist_ok=True)

        # 3. Process all Markdown files in the gist folder
        for root, _, files in os.walk(gist_path):
            if "images" in root: # Skip the images folder itself
                continue
            for file in files:
                if file.endswith(".md"):
                    process_markdown_file(os.path.join(root, file), images_dir)

    print("\n[✔] Backup complete! All gists and images are safely stored locally.")

if __name__ == "__main__":
    main()
