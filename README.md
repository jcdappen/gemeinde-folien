# 🎬 Gemeinde Folien - Automatischer Folien-Generator

> Automatisches Folien-Generator-System für die Gemeinde in der Konkordia

Generiert täglich professionelle PNG-Folien aus iCal-Kalenderdaten für Gottesdienst-Ansagen und Beamer-Präsentationen.

---

## 🌐 Live URL

**Web-Viewer:** https://jcdappen.github.io/gemeinde-folien/

---

## ✨ Features

- ✅ **Vollautomatisch**: Täglich um 06:00 Uhr neue Folien
- 🎨 **Gemeinde-Design**: Roter Banner, hellgrauer Footer, QR-Code
- 📅 **iCal-Integration**: Synchronisiert mit News---Aktuelles Repository
- 🖼️ **Full HD**: 1920×1080px PNG-Folien
- 📺 **Web-Viewer**: Auto-Rotation, Tastatur-Navigation, Vollbild
- ⏱️ **Smart-Timing**: 10s Termine, 6s Info-Folien
- 🔄 **3:1 Rhythmus**: Automatische Info-Folien-Einstreuung

---

## 🏗️ Projektstruktur

```
gemeinde-folien/
├── .github/
│   └── workflows/
│       ├── sync-ical.yml           # Synchronisiert iCal alle 2h
│       └── generate-slides.yml     # Generiert Folien täglich um 06:00
├── src/
│   ├── generator.py                # Python-Script für Folien-Generierung
│   └── requirements.txt            # Dependencies
├── slides/                         # Generierte PNG + Info-Folien (JPG)
│   ├── slide_00_titel.png         # (automatisch)
│   ├── slide_01_*.png             # (automatisch)
│   ├── slide1.jpg                 # Info-Folie
│   └── ...
├── viewer/
│   └── index.html                 # Web-Präsentation
├── *.ics                          # iCal-Kalender (sync von News repo)
└── README.md
```

---

## 🚀 Setup & Installation

### 1. GitHub Pages aktivieren

1. Gehe zu: **Repository Settings** → **Pages**
2. Unter **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `gh-pages` + `/ (root)`
   - Klicke **Save**

### 2. Workflows testen

**iCal Sync testen:**
1. Gehe zu `Actions` → `Sync iCal Feeds`
2. Klicke `Run workflow`
3. Prüfe dass `.ics` Dateien aktualisiert wurden

**Folien-Generator testen:**
1. Gehe zu `Actions` → `Generate Slides`
2. Klicke `Run workflow`
3. Warte ~2 Minuten
4. Öffne: https://jcdappen.github.io/gemeinde-folien/

---

## ⚙️ Workflows

### 📅 Sync iCal Feeds (`sync-ical.yml`)

- **Trigger:** Alle 2 Stunden + manuell
- **Quelle:** `jcdappen/News---Aktuelles` Repository
- **Ziel:** Lokale `.ics` Dateien
- **Dateien:**
  - `gottesdienst.ics`
  - `kinder.ics`
  - `senioren.ics`
  - `jugend.ics`
  - `sonstige.ics`

### 🎬 Generate Slides (`generate-slides.yml`)

- **Trigger:** Täglich 06:00 Uhr + bei iCal-Änderungen + manuell
- **Prozess:**
  1. Parsed iCal-Dateien
  2. Filtert Events (nächste 14 Tage)
  3. Generiert PNG-Folien
  4. Committed zu `main` Branch
  5. Deployed zu `gh-pages` Branch
- **Output:** ~15-25 Folien (je nach Terminen)

---

## 🎨 Folien-Design

### Layout
```
┌─────────────────────────────────────┐
│   [Dunkler strukturierter BG]      │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  VERANSTALTUNG (Rot)         │ │ ← Roter Banner
│  └───────────────────────────────┘ │
│                                     │
│  Beschreibung...                   │ ← Weiß, zentriert
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Sonntag              ┌──────┐ │ │ ← Hellgrauer Footer
│  │ 11. Januar 2026      │  QR  │ │ │
│  │ 🕐 09:30 - 09:45    │ Code │ │ │
│  │ 📍 Adresse...        └──────┘ │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Typografie
- **Titel:** 100-120px (Bold, Rot, Großbuchstaben)
- **Datum:** 85px (Bold, Schwarz) ← Sehr prominent!
- **Beschreibung:** 42px (Regular, Weiß)
- **Wochentag:** 38px (Regular, Schwarz)
- **Details:** 36px (Regular, Schwarz)

### Farben
- **Gemeinde-Rot:** `#bb2232` (RGB: 187, 34, 50)
- **Footer:** `rgb(240, 240, 240)` (Hellgrau)
- **Text:** Schwarz / Weiß

---

## 📝 Info-Folien hinzufügen

1. Erstelle JPG-Folie (1920×1080px)
2. Benenne sie: `slideX.jpg` (z.B. `slide7.jpg`)
3. Lege sie in `slides/` Ordner
4. Commit & Push:

```bash
git add slides/slide7.jpg
git commit -m "Neue Info-Folie hinzugefügt"
git push
```

**Rhythmus:** Info-Folien werden automatisch nach jedem 3. Event eingestreut.

---

## 🖥️ Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/jcdappen/gemeinde-folien.git
cd gemeinde-folien

# Dependencies installieren
pip install -r src/requirements.txt

# Folien generieren
python src/generator.py

# Viewer öffnen
open viewer/index.html
# oder
python -m http.server 8000
# dann: http://localhost:8000/viewer/
```

---

## 🔧 Konfiguration anpassen

### Zeitfilter ändern
```python
# In src/generator.py, Zeile ~67
DAYS_AHEAD = 30  # Termine der nächsten 30 Tage (statt 14)
```

### Workflow-Zeiten ändern
```yaml
# In .github/workflows/generate-slides.yml
schedule:
  - cron: '0 5 * * *'  # Um 05:00 Uhr statt 06:00
```

### Farben anpassen
```python
# In src/generator.py, Config-Klasse
GEMEINDE_ROT = (200, 50, 50)  # Anderer Rotton
```

---

## 🌐 Web-Viewer Bedienung

### Tastatur-Shortcuts
- `←` / `→` - Vorherige/Nächste Folie
- `Leertaste` - Pause/Play
- `F` - Vollbild
- `ESC` - Vollbild beenden
- `H` - Hilfe
- `R` - Neu laden

### Features
- Auto-Rotation (10s Termine, 6s Info)
- Progress Bar
- Seitenzahl-Anzeige
- Auto-Hide Controls

---

## 🎓 Verwendung

### Für Gottesdienst-Beamer
1. Öffne: https://jcdappen.github.io/gemeinde-folien/
2. Drücke `F` für Vollbild
3. Auto-Rotation läuft automatisch

### Für ProPresenter
**Option A:** Web-URL einbinden
- `Media` → `New Web`
- URL: https://jcdappen.github.io/gemeinde-folien/

**Option B:** PNG-Folien herunterladen
- Lade Folien von: https://jcdappen.github.io/gemeinde-folien/slides/
- Importiere als Bilder in ProPresenter

---

## 🔍 Troubleshooting

### Keine Folien werden generiert

1. Prüfe Action Logs: `Actions` → `Generate Slides`
2. Prüfe iCal-Dateien: Sind Events vorhanden?
3. Lokales Testing: `python src/generator.py`

### Web-Viewer zeigt keine Folien

1. Warte 2-3 Minuten nach Deployment
2. GitHub Pages aktiviert? Settings → Pages
3. Branch ist `gh-pages`?
4. Cache leeren: Strg+Shift+R

### iCal-Sync schlägt fehl

1. Prüfe dass News---Aktuelles Repository public ist
2. Prüfe URLs in `sync-ical.yml`
3. Manuelles Sync: Actions → Sync iCal Feeds → Run workflow

---

## 📊 Automatisierung

```
Jeden Tag:
├─ 00:00, 02:00, 04:00... → iCal-Sync läuft
├─ 06:00 → Folien-Generator läuft
│   ├─ Parsed iCal-Dateien
│   ├─ Generiert PNG-Folien
│   ├─ Committed zu main
│   └─ Deployed zu GitHub Pages
└─ Live URL wird aktualisiert
```

**Ohne manuelle Arbeit! ✨**

---

## 📄 Lizenz

Dieses Projekt ist für die **Gemeinde in der Konkordia** erstellt.

## 🆘 Support

Bei Fragen oder Problemen:
- [GitHub Issues](https://github.com/jcdappen/gemeinde-folien/issues)
- [Gemeinde Konkordia](https://gemeindekonkordia.de)

---

**Erstellt mit ❤️ für die Gemeinde in der Konkordia**

*Automatisiert • Professionell • Einfach zu bedienen*
