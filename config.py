import os

# Konfiguration für das Backup-Skript
# Passe die Werte an oder lege sie als Umgebungsvariablen fest.
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "YOUR_GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN")
BACKUP_DIR = os.getenv("BACKUP_DIR", "./my_gists_backup")
