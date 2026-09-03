from pathlib import Path
required = [
    "segmentation_colab.ipynb",
    "segmentation_local.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "config.example.json",
]
missing = [x for x in required if not Path(x).exists()]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing))
print("Repository structure OK")
