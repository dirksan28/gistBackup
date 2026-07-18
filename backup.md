The following script completes all three steps automatically in one go:
- It connects to your GitHub account and downloads all your gists recursively.
- It scans each gist for embedded GitHub image links.
- It downloads the images, stores them locally in the respective gist folder, and rewrites the Markdown links to the local paths.

RequirementsYou need only two things in the terminal:
```
pip install requests
```

Additionally, you need a Personal Access Token (Classic) from GitHub with the gist scope. 
You can create this in your GitHub settings under Developer Settings > Personal Access Tokens.

The resulting folder structureAfter running the script, the script organizes your gists neatly sorted. Each gist gets its own media folder:
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
