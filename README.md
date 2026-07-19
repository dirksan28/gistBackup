# Gist Backup Tool
A Python-based tool that recursively downloads and backs up all your gists stored on GitHub, so you can keep a local copy of every snippet.

## General
The script completes all three steps to get your gists into your local filesystem:
- It connects to your GitHub account and downloads all your gists recursively.
- It scans each gist for embedded GitHub image links.
- It downloads the images, stores them locally in the respective gist folder, and rewrites the Markdown links to the local paths.

## Config
### Requirements:
```
pip install requests
```

### GIT Gist Credentials
Additionally, you need a Personal Access Token (Classic) from GitHub with the gist scope. 
You can create this in your GitHub settings under Developer Settings > Personal Access Tokens.

>[!IMPORTANT]
>Please copy cofig.py.example to config.py and fill in your GITHUB-Gist-Token and Username.

## The resulting folder structure: 
After running the script, the script organizes your gists neatly sorted. Each gist gets its own media folder:
```
my_gists_backup/
├── Project-Notes_a1b2c3d4e5f6.../
│   ├── README.md            <-- Links now point to "images/image1.png"
│   ├── script.py
│   └── images/
│       └── image1.png        <-- Local image file
└── API-Documentation_7r8s9t0.../
    ├── doc.md
    └── images/
        └── diagram.jpg
```

## HowTo Generate Gist Access Token
You create a “Personal Access Token (classic)” with the gist scope from your account settings, not from an individual repository, by navigating to Developer settings → Personal access tokens → Tokens (classic) and generating a new token with only the gist scope enabled.

## Step‑by‑step: create a classic PAT with `gist` scope

1. **Sign in to GitHub**  
   Go to `https://github.com` and log in with your user account.

2. **Open your account settings**  
   - Click your **profile picture** in the top‑right corner.  
   - Click **Settings** (these are account‑level settings, not repo settings).

3. **Open Developer settings**  
   In the left sidebar of the settings page, scroll down and click **Developer settings**.

4. **Go to Personal access tokens (classic)**  
   - In the left sidebar, click **Personal access tokens**.  
   - Then select the **Tokens (classic)** tab (if it’s not already active).

5. **Start creating a new token**  
   - Click **Generate new token** (or **Generate new token (classic)**).  
   - Give the token a descriptive **name**, e.g. `gist-token`.  
   - Choose an **expiration** (e.g. 30 days, 90 days, or “No expiration” depending on your needs and any org policies).

6. **Select only the `gist` scope**  
   In the list of scopes/permissions:
   - Check the box for **`gist`**.  
   - Leave all other scopes **unchecked** if you want the token to be usable *only* for Gists (read/write Gists, using the Gist API, etc.).

7. **Generate the token**  
   - Scroll down and click **Generate token**.  
   - GitHub will show you the token value once (something like `ghp_xxxxxxxxxxxxx`).  
   - **Copy it immediately** and store it somewhere secure (password manager, environment variable, etc.), because you won’t be able to see it again later.

8. **Use the token**  
   - In CLI tools or scripts that need access to Gists, use this token instead of a password, or configure it as an environment variable (e.g. `GITHUB_TOKEN` or a tool‑specific variable).  
   - Anywhere you previously would have used a GitHub password for Gist/API access over HTTPS, use this PAT with `gist` scope instead.
