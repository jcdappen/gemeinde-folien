#!/usr/bin/env python3
"""
Gemeinde Folien - Slide Downloader
Lädt alle aktuellen PNG-Slides vom GitHub Repository herunter
"""

import os
import sys
import requests
from pathlib import Path
from urllib.parse import quote

# Konfiguration
REPO_OWNER = "jcdappen"
REPO_NAME = "gemeinde-folien"
BRANCH = "claude/church-slide-generator-1Eawn"
SLIDES_DIR = "slides"
OUTPUT_DIR = "downloaded_slides"

def get_file_list():
    """Holt die Liste aller Dateien im slides/ Ordner vom GitHub"""
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{SLIDES_DIR}?ref={BRANCH}"

    print(f"🔍 Hole Dateiliste von GitHub...")
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"❌ Fehler beim Abrufen der Dateiliste: {response.status_code}")
        sys.exit(1)

    files = response.json()

    # Filtere nur PNG-Dateien
    png_files = [f for f in files if f['name'].endswith('.png')]

    print(f"✅ {len(png_files)} PNG-Slides gefunden")
    return png_files

def download_file(file_info, output_dir):
    """Lädt eine einzelne Datei herunter"""
    file_name = file_info['name']
    download_url = file_info['download_url']

    output_path = output_dir / file_name

    print(f"⬇️  Lade {file_name}...", end=' ')

    try:
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        file_size = len(response.content) / 1024  # KB
        print(f"✅ ({file_size:.1f} KB)")
        return True

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def main():
    """Hauptfunktion"""
    print("=" * 60)
    print("🎬 Gemeinde Folien - Slide Downloader")
    print("=" * 60)
    print()

    # Erstelle Output-Verzeichnis
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Zielverzeichnis: {output_dir.absolute()}")
    print()

    # Hole Dateiliste
    files = get_file_list()
    print()

    # Lade alle Dateien herunter
    success_count = 0
    fail_count = 0

    for file_info in files:
        if download_file(file_info, output_dir):
            success_count += 1
        else:
            fail_count += 1

    # Zusammenfassung
    print()
    print("=" * 60)
    print(f"✅ Download abgeschlossen!")
    print(f"   Erfolgreich: {success_count} Dateien")
    if fail_count > 0:
        print(f"   ❌ Fehlgeschlagen: {fail_count} Dateien")
    print(f"   📁 Gespeichert in: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Download abgebrochen")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unerwarteter Fehler: {e}")
        sys.exit(1)
