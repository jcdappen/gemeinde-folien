#!/bin/bash
###############################################################################
# Gemeinde Folien - Slide Downloader (Bash Version)
# Lädt alle aktuellen PNG-Slides vom GitHub Repository herunter
###############################################################################

REPO_OWNER="jcdappen"
REPO_NAME="gemeinde-folien"
BRANCH="claude/church-slide-generator-1Eawn"
OUTPUT_DIR="downloaded_slides"

echo "============================================================"
echo "🎬 Gemeinde Folien - Slide Downloader"
echo "============================================================"
echo ""

# Erstelle Output-Verzeichnis
mkdir -p "$OUTPUT_DIR"
echo "📁 Zielverzeichnis: $(pwd)/$OUTPUT_DIR"
echo ""

# Hole Dateiliste von GitHub API
echo "🔍 Hole Dateiliste von GitHub..."
API_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/contents/slides?ref=$BRANCH"

# Hole JSON und extrahiere PNG-Dateien
FILES=$(curl -s "$API_URL" | grep -o '"download_url":"[^"]*\.png"' | sed 's/"download_url":"//g' | sed 's/"//g')

if [ -z "$FILES" ]; then
    echo "❌ Keine PNG-Dateien gefunden!"
    exit 1
fi

FILE_COUNT=$(echo "$FILES" | wc -l)
echo "✅ $FILE_COUNT PNG-Slides gefunden"
echo ""

# Lade alle Dateien herunter
SUCCESS=0
FAILED=0

for URL in $FILES; do
    FILENAME=$(basename "$URL")
    echo -n "⬇️  Lade $FILENAME... "

    if curl -s -L -o "$OUTPUT_DIR/$FILENAME" "$URL"; then
        SIZE=$(du -h "$OUTPUT_DIR/$FILENAME" | cut -f1)
        echo "✅ ($SIZE)"
        ((SUCCESS++))
    else
        echo "❌ Fehler"
        ((FAILED++))
    fi
done

# Zusammenfassung
echo ""
echo "============================================================"
echo "✅ Download abgeschlossen!"
echo "   Erfolgreich: $SUCCESS Dateien"
if [ $FAILED -gt 0 ]; then
    echo "   ❌ Fehlgeschlagen: $FAILED Dateien"
fi
echo "   📁 Gespeichert in: $(pwd)/$OUTPUT_DIR"
echo "============================================================"
