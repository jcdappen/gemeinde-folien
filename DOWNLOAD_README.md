# 📥 Slides Download Scripts

Automatische Download-Scripts für die aktuellen Gemeinde-Folien vom GitHub Repository.

## 🚀 Verwendung

### Python-Script (Empfohlen für alle Systeme)

**Voraussetzungen:**
- Python 3.6+
- `requests` Bibliothek

```bash
# Installation von requests (falls noch nicht vorhanden)
pip install requests

# Script ausführen
python download_slides.py
```

**Ausgabe:** Alle Slides werden in den Ordner `downloaded_slides/` heruntergeladen.

---

### Bash-Script (Linux/Mac)

**Voraussetzungen:**
- `curl` (meist vorinstalliert)

```bash
# Script ausführbar machen
chmod +x download_slides.sh

# Script ausführen
./download_slides.sh
```

**Oder direkt:**
```bash
bash download_slides.sh
```

---

### Windows Batch-Script

**Voraussetzungen:**
- `curl` (ab Windows 10 vorinstalliert)

```cmd
# Doppelklick auf die Datei oder:
download_slides.bat
```

---

## 📁 Output

Alle Scripts laden die Slides in den Ordner:
```
downloaded_slides/
├── slide_00_titel.png
├── slide_01_Gebet_vor_dem_Gottes_11Jan.png
├── slide_02_Gottesdienst_11Jan.png
├── ...
└── slide_20_info.png
```

## 🔧 Konfiguration

Falls du einen anderen Branch verwenden möchtest, ändere diese Zeilen in den Scripts:

**Python:**
```python
BRANCH = "dein-branch-name"
```

**Bash:**
```bash
BRANCH="dein-branch-name"
```

**Windows:**
```batch
set BRANCH=dein-branch-name
```

## ⚠️ Problembehandlung

### Script kann nicht ausgeführt werden

**Linux/Mac:**
```bash
chmod +x download_slides.sh download_slides.py
```

### "requests" Modul nicht gefunden

```bash
pip install requests
```

### curl nicht verfügbar (Windows)

Verwende das Python-Script oder installiere curl:
- https://curl.se/windows/

## 📊 Beispielausgabe

```
============================================================
🎬 Gemeinde Folien - Slide Downloader
============================================================

📁 Zielverzeichnis: /path/to/downloaded_slides

🔍 Hole Dateiliste von GitHub...
✅ 21 PNG-Slides gefunden

⬇️  Lade slide_00_titel.png... ✅ (30.5 KB)
⬇️  Lade slide_01_Gebet_vor_dem_Gottes_11Jan.png... ✅ (79.2 KB)
⬇️  Lade slide_02_Gottesdienst_11Jan.png... ✅ (97.1 KB)
...

============================================================
✅ Download abgeschlossen!
   Erfolgreich: 21 Dateien
   📁 Gespeichert in: /path/to/downloaded_slides
============================================================
```

## 🔄 Automatische Updates

Um die Slides regelmäßig zu aktualisieren, kannst du das Script per Cronjob (Linux/Mac) oder Task Scheduler (Windows) automatisch ausführen lassen.

**Linux Cron Beispiel (täglich um 7:00 Uhr):**
```bash
0 7 * * * cd /pfad/zum/repo && python download_slides.py
```

---

**Erstellt für die Gemeinde in der Konkordia** ❤️
