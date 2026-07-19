# gistBackup
Local, Fully Renderable Backups of Your GitHub Gists

## Purpose
GitHub Gists are great for sharing snippets, notes, and small projects — but they rely on GitHub’s availability, and any externally linked images or media can disappear over time. gistBackup ensures your Gists remain fully accessible by creating complete local copies, including all files and downloaded media, with rewritten URLs so everything renders correctly offline.

This is especially useful if you maintain technical notes, documentation, or code examples that include screenshots or diagrams. For example, a Gist explaining a debugging process with embedded images will remain fully functional even years later, regardless of whether the original image host still exists.

The backed‑up Gists can also be stored as normal Git repositories, making long‑term archiving, versioning, or further development straightforward.

`backup.py` creates **complete local backups** of your GitHub Gists—including all files, folder structures, and **linked media**.  
Backups are stored so they can be **rendered locally exactly as on GitHub**, including images and other media, even when you’re offline.

The project also **downloads media referenced in your Gists** and **rewrites their URLs** to point to local files.  
If desired, the backed‑up Gists can be **used as normal Git repositories**, making it easy to archive, version, or further develop them

---

## Features

- **Backup of your GitHub Gists** via the GitHub API  
- **Local folder structure** mirroring each Gist  
- **Download of linked media** (e.g. images in Markdown)  
- **URL conversion** so Markdown files reference local media paths  
- **Offline‑renderable copies** of your Gists  
- **Can be turned into regular Git repos** for further use

---

## Configuration

Configuration is limited to three core options:

- **Git username** – the GitHub user whose Gists will be backed up  
- **Git token (Personal Access Token)** – used to authenticate against the GitHub API  
- **Backup directory** – the local directory where all Gist backups are stored  

You can configure these either via `config.py` or environment variables.

### 1. Using `config.py`

A template file `config.py.example` is provided.

```bash
cp config.py.example config.py
```

Then edit `config.py` and set:

- your GitHub username,  
- your GitHub Personal Access Token,  
- your desired backup directory.

### 2. Using environment variables

You can also configure the script via environment variables, for example:

```bash
export GISTBACKUP_USERNAME="<YOUR_GITHUB_USERNAME>"
export GISTBACKUP_TOKEN="<YOUR_GITHUB_TOKEN>"
export GISTBACKUP_OUTPUT="./backup"

python backup.py
```

This is convenient for shells, scripts, or CI pipelines.

#### GIT Gist Credentials
You need a Personal Access Token (Classic) from GitHub with the gist scope to give the script access to your gists. You can create this in your GitHub settings under Developer Settings > Personal Access Tokens. See [HowTo Generate Gist Access Token](#howto-generate-gist-access-token) for more details.

## How it works
1. The script reads configuration from environment variables and/or `config.py`.  
2. It connects to the GitHub API using your username and token.  
3. All Gists for that user are fetched and stored in the backup directory.  
4. Markdown files are scanned for linked media:
   - media files are downloaded,
   - URLs are rewritten to point to the local copies.  
5. The result is a **self‑contained, locally renderable backup** of each Gist, which can also be managed as a normal Git repository if you choose.

## How to run the script

**Example using environment variables:**

```bash
export GISTBACKUP_USERNAME="your-username"
export GISTBACKUP_TOKEN="ghp_XXXXXXXXXXXXXXXXXXXX"
export GISTBACKUP_OUTPUT="./backup"

python backup.py
```

**Example using `config.py`:**

```bash
python backup.py
```

## Example backup structure

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

All Markdown files reference the downloaded media, so they render correctly without any network access.

---

## Resources
### HowTo Generate Gist Access Token
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
