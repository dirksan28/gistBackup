import os
import re
import requests
import subprocess

from config import GITHUB_USERNAME, GITHUB_TOKEN, BACKUP_DIR

# GitHub API URL für die Gists des Nutzers
API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/gists"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Regex für GitHub-Bild-URLs im Markdown
img_regex = re.compile(r'(!\[.*?\]\()(https://(?:user-images\.githubusercontent\.com|github-production-user-asset-[^\s)]+)[^\s)]*)(\))')

os.makedirs(BACKUP_DIR, exist_ok=True)

def fetch_gists():
    """Holt alle Gists über die GitHub API (inkl. Pagination)"""
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
    """Scannt eine MD-Datei, lädt Bilder herunter und passt Links an"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = img_regex.findall(content)
    if not matches:
        return

    new_content = content
    for prefix, url, suffix in matches:
        # Sauberen Dateinamen extrahieren
        img_name = url.split("/")[-1].split("?")[0]
        local_img_path = os.path.join(images_dir, img_name)

        # Bild herunterladen, falls noch nicht vorhanden
        if not os.path.exists(local_img_path):
            try:
                print(f"  -> Lade Bild herunter: {img_name}")
                img_data = requests.get(url).content
                with open(local_img_path, "wb") as img_file:
                    img_file.write(img_data)
            except Exception as e:
                print(f"  [!] Fehler beim Bild-Download {url}: {e}")
                continue

        # Relativen Pfad für das Markdown berechnen (zeigt auf den lokalen 'images' Ordner)
        # Da der 'images' Ordner direkt im Gist-Ordner liegt, reicht 'images/name.png'
        rel_path = f"images/{img_name}"
        old_link = f"{prefix}{url}{suffix}"
        new_link = f"{prefix}{rel_path}{suffix}"
        new_content = new_content.replace(old_link, new_link)

    # Datei aktualisieren
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  -> Links in {os.path.basename(file_path)} erfolgreich angepasst.")

def main():
    print("Starte Gist-Backup-Prozess...")
    gists = fetch_gists()
    print(f"{len(gists)} Gists gefunden. Beginne Download via Git...")

    for gist in gists:
        gist_id = gist["id"]
        # Beschreibung als Ordnername nutzen, falls vorhanden, sonst die ID
        description = gist["description"] or "Unbenanntes_Gist"
        # Ordnernamen von ungültigen Zeichen bereinigen
        safe_desc = re.sub(r'[^\w\-_.]', '_', description)[:50]
        gist_folder_name = f"{safe_desc}_{gist_id}"
        gist_path = os.path.join(BACKUP_DIR, gist_folder_name)

        # 1. Gist per Git klonen oder aktualisieren
        if os.path.exists(gist_path):
            print(f"\nAktualisiere: {gist_folder_name}")
            subprocess.run(["git", "-C", gist_path, "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"\nKlone: {gist_folder_name}")
            # Nutzt das Token in der URL, um auch private Gists klonen zu können
            clone_url = gist["git_pull_url"].replace("https://", f"https://{GITHUB_TOKEN}@")
            subprocess.run(["git", "clone", clone_url, gist_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Bilderverzeichnis innerhalb des Gists erstellen
        images_dir = os.path.join(gist_path, "images")
        os.makedirs(images_dir, exist_ok=True)

        # 3. Alle Markdown-Dateien im Gist-Ordner verarbeiten
        for root, _, files in os.walk(gist_path):
            if "images" in root: # Den Bilder-Ordner selbst überspringen
                continue
            for file in files:
                if file.endswith(".md"):
                    process_markdown_file(os.path.join(root, file), images_dir)

    print("\n[✔] Komplettes Backup abgeschlossen! Alle Gists und Bilder sind lokal gesichert.")

if __name__ == "__main__":
    main()
