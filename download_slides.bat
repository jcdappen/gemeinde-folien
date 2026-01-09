@echo off
REM ============================================================================
REM Gemeinde Folien - Slide Downloader (Windows Version)
REM Lädt alle aktuellen PNG-Slides vom GitHub Repository herunter
REM ============================================================================

setlocal enabledelayedexpansion

set REPO_OWNER=jcdappen
set REPO_NAME=gemeinde-folien
set BRANCH=claude/church-slide-generator-1Eawn
set OUTPUT_DIR=downloaded_slides

echo ============================================================
echo 🎬 Gemeinde Folien - Slide Downloader
echo ============================================================
echo.

REM Erstelle Output-Verzeichnis
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
echo 📁 Zielverzeichnis: %CD%\%OUTPUT_DIR%
echo.

REM Prüfe ob curl verfügbar ist
where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ curl ist nicht verfügbar. Bitte installiere curl oder verwende das Python-Script.
    pause
    exit /b 1
)

echo 🔍 Hole Dateiliste von GitHub...

REM Hole Dateiliste und lade alle PNG-Dateien herunter
set API_URL=https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/contents/slides?ref=%BRANCH%

REM Erstelle temporäre Datei für die JSON-Response
set TEMP_FILE=%TEMP%\github_api_response.json
curl -s "%API_URL%" > "%TEMP_FILE%"

REM Zähle Dateien
for /f "tokens=*" %%i in ('findstr /c:"\"download_url\"" "%TEMP_FILE%" ^| findstr /c:".png" ^| find /c /v ""') do set FILE_COUNT=%%i

if %FILE_COUNT% equ 0 (
    echo ❌ Keine PNG-Dateien gefunden!
    del "%TEMP_FILE%"
    pause
    exit /b 1
)

echo ✅ %FILE_COUNT% PNG-Slides gefunden
echo.

REM Lade alle PNG-Dateien herunter
set SUCCESS=0
set FAILED=0

for /f "tokens=2 delims=:" %%i in ('findstr /c:"\"download_url\"" "%TEMP_FILE%" ^| findstr /c:".png"') do (
    set URL=%%i
    set URL=!URL:"=!
    set URL=!URL: =!
    set URL=!URL:,=!

    for %%f in ("!URL!") do set FILENAME=%%~nxf

    echo ⬇️  Lade !FILENAME!...
    curl -s -L -o "%OUTPUT_DIR%\!FILENAME!" "!URL!"

    if !errorlevel! equ 0 (
        set /a SUCCESS+=1
        echo    ✅ Erfolgreich
    ) else (
        set /a FAILED+=1
        echo    ❌ Fehler
    )
)

REM Aufräumen
del "%TEMP_FILE%"

REM Zusammenfassung
echo.
echo ============================================================
echo ✅ Download abgeschlossen!
echo    Erfolgreich: %SUCCESS% Dateien
if %FAILED% gtr 0 (
    echo    ❌ Fehlgeschlagen: %FAILED% Dateien
)
echo    📁 Gespeichert in: %CD%\%OUTPUT_DIR%
echo ============================================================

pause
