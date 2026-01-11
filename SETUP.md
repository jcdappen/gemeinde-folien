# 🚀 Setup-Anleitung für gemeinde-folien Repository

## ✅ Was bereits erledigt ist:

- ✅ Repository lokal initialisiert
- ✅ Alle Dateien erstellt und committed
- ✅ Workflows konfiguriert
- ✅ README dokumentiert

---

## 📋 Nächste Schritte:

### 1. Repository zu GitHub pushen

```bash
cd /home/user/gemeinde-folien

# Push zum GitHub Repository
git push -u origin main
```

**Falls Push fehlschlägt mit Authentifizierungsfehler:**

Option A: Verwende den lokalen Git-Proxy (Claude Code):
- Der Push sollte automatisch über den Proxy funktionieren

Option B: Erstelle Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Rechte: `repo` (alle Unterrechte)
4. Token kopieren
5. Bei Push nach Username/Password gefragt → Token als Password eingeben

---

### 2. GitHub Pages aktivieren

Nach erfolgreichem Push:

1. Gehe zu: https://github.com/jcdappen/gemeinde-folien/settings/pages
2. Unter **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `gh-pages` + `/ (root)`
   - Klicke **Save**

**Wichtig:** Beim ersten Mal muss der Branch `gh-pages` erst erstellt werden!

---

### 3. Workflows manuell auslösen (Erstmalig)

#### a) iCal-Dateien synchronisieren:

1. Gehe zu: https://github.com/jcdappen/gemeinde-folien/actions
2. Wähle Workflow: **"Sync iCal Feeds"**
3. Klicke: **"Run workflow"** → **"Run workflow"**
4. Warte ~30 Sekunden

#### b) Folien generieren und deployen:

1. Gehe zu: https://github.com/jcdappen/gemeinde-folien/actions
2. Wähle Workflow: **"Generate Slides"**
3. Klicke: **"Run workflow"** → **"Run workflow"**
4. Warte ~2-3 Minuten

Dieser Workflow wird:
- PNG-Folien generieren
- `gh-pages` Branch erstellen (falls nicht vorhanden)
- Viewer deployen

---

### 4. GitHub Pages konfigurieren (nachdem gh-pages Branch existiert)

1. Gehe zurück zu: https://github.com/jcdappen/gemeinde-folien/settings/pages
2. Unter **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `gh-pages` (sollte jetzt verfügbar sein) + `/ (root)`
   - Klicke **Save**

---

### 5. URL testen

Nach ~2 Minuten sollte die Seite verfügbar sein:

**Live URL:** https://jcdappen.github.io/gemeinde-folien/

Falls "404 Not Found":
- Warte weitere 2 Minuten
- Cache leeren: Strg+Shift+R
- Prüfe dass GitHub Pages aktiviert ist

---

## 🔄 Automatisierung

Ab jetzt läuft alles automatisch:

```
┌─────────────────────────────────────────┐
│ Alle 2 Stunden:                         │
│ → iCal-Dateien synchronisieren          │
│   (von News---Aktuelles Repository)     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Täglich um 06:00 Uhr:                   │
│ → Folien generieren                     │
│ → PNG-Folien committen                  │
│ → Zu GitHub Pages deployen              │
│ → Live URL automatisch aktualisiert     │
└─────────────────────────────────────────┘
```

---

## 📝 Info-Folien hinzufügen

1. Neue JPG-Folie erstellen (1920×1080px)
2. Benennen: `slide7.jpg`, `slide8.jpg`, etc.
3. In `slides/` Ordner ablegen
4. Committen und pushen:

```bash
cd /home/user/gemeinde-folien
git add slides/slide7.jpg
git commit -m "Neue Info-Folie hinzugefügt"
git push
```

5. Beim nächsten Workflow-Lauf (06:00 Uhr) wird sie automatisch integriert!

---

## 🔧 Troubleshooting

### Problem: Push schlägt fehl

```bash
# Prüfe Remote
cd /home/user/gemeinde-folien
git remote -v

# Sollte anzeigen:
# origin  https://github.com/jcdappen/gemeinde-folien.git (fetch)
# origin  https://github.com/jcdappen/gemeinde-folien.git (push)
```

Falls Remote falsch:
```bash
git remote set-url origin https://github.com/jcdappen/gemeinde-folien.git
```

### Problem: gh-pages Branch wird nicht erstellt

**Lösung:**
- Workflow "Generate Slides" manuell nochmal ausführen
- Prüfe Action Logs auf Fehler
- Branch sollte nach erfolgreichem Lauf existieren

### Problem: Folien werden nicht generiert

**Lösung:**
1. Prüfe dass iCal-Dateien existieren: https://github.com/jcdappen/gemeinde-folien
2. Lasse "Sync iCal Feeds" Workflow laufen
3. Dann "Generate Slides" Workflow

---

## 📞 Support

Bei Problemen:
- GitHub Issues: https://github.com/jcdappen/gemeinde-folien/issues
- Prüfe Action Logs: https://github.com/jcdappen/gemeinde-folien/actions

---

**Viel Erfolg! 🎉**
