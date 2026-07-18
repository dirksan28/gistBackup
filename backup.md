Das folgende Skript erledigt alle drei Schritte vollautomatisch in einem Rutsch:
- Es verbindet sich mit Ihrem GitHub-Account und lädt alle Ihre Gists rekursiv herunter.
- Es scannt jedes Gist nach eingebetteten GitHub-Bildlinks.
- Es lädt die Bilder herunter, speichert sie lokal im jeweiligen Gist-Ordner ab und schreibt die Markdown-Links auf die lokalen Pfade um.

VoraussetzungenSie benötigen lediglich zwei Dinge im Terminal:
```
pip install requests
```

Zudem benötigen Sie einen Personal Access Token (Classic) von GitHub mit dem Recht (Scope) gist. 
Diesen können Sie in Ihren GitHub-Einstellungen unter Developer Settings > Personal Access Tokens erstellen.

Die resultierende OrdnerstrukturNach dem Durchlauf legt das Skript Ihre Gists ordentlich sortiert ab. Jedes Gist erhält einen eigenen Medienordner:
```
my_gists_backup/
├── Projekt-Notizen_a1b2c3d4e5f6.../
│   ├── README.md            <-- Links zeigen jetzt auf "images/bild1.png"
│   ├── skript.py
│   └── images/
│       └── bild1.png        <-- Lokale Bilddatei
└── API-Dokumentation_7r8s9t0.../
    ├── doc.md
    └── images/
        └── diagramm.jpg
```

