#!/usr/bin/env python3
"""
Automatischer Folien-Generator für Gemeinde in der Konkordia
Generiert PNG-Folien aus iCal-Daten im Gemeinde-Design
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from icalendar import Calendar
from dateutil import tz
import qrcode

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Konfiguration
class Config:
    # Farben
    GEMEINDE_ROT = (187, 34, 50)  # #bb2232
    WEISS = (255, 255, 255)
    HINTERGRAU = (245, 245, 245)
    TEXT_GRAU = (51, 51, 51)
    SCHWARZ = (0, 0, 0)

    # Assets
    HINTERGRUND_URL = "https://storage2.snappages.site/S74RKH/assets/files/hintergrund_Termine.jpg"
    QR_CODE_URL = "https://storage2.snappages.site/S74RKH/assets/files/QR_news.png"

    # Layout
    WIDTH = 1920
    HEIGHT = 1080

    # Banner
    BANNER_HEIGHT_MIN = 200
    BANNER_HEIGHT_MAX = 350
    BANNER_PADDING = 40

    # Footer
    FOOTER_HEIGHT = 280
    FOOTER_PADDING = 40
    QR_SIZE = 150

    # Schriften
    TITLE_FONT_SIZE = 100
    TITLE_FONT_SIZE_MIN = 60
    DESC_FONT_SIZE = 42
    FOOTER_FONT_SIZE = 38

    # iCal URLs (lokale Dateien)
    ICAL_FILES = [
        "gottesdienst.ics",
        "kinder.ics",
        "senioren.ics",
        "jugend.ics",
        "sonstige.ics"
    ]

    # Ausgabe
    OUTPUT_DIR = "slides"
    INFO_SLIDES_DIR = "slides"  # Info-Folien liegen bereits hier

    # Zeitzone
    TIMEZONE = tz.gettz('Europe/Berlin')

    # Event Filter
    DAYS_AHEAD = 14  # Nur Termine der nächsten 14 Tage

    # Deutsche Namen
    WOCHENTAGE = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }

    MONATE = {
        1: "Januar", 2: "Februar", 3: "März", 4: "April",
        5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
        9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
    }


class AssetManager:
    """Verwaltet Assets (Bilder, Fonts)"""

    def __init__(self):
        self.background = None
        self.qr_code = None
        self.fonts = {}
        self._load_assets()

    def _load_assets(self):
        """Lädt alle Assets"""
        self._load_background()
        self._load_qr_code()
        self._load_fonts()

    def _load_background(self):
        """Lädt Hintergrundbild"""
        try:
            logger.info(f"Lade Hintergrundbild von {Config.HINTERGRUND_URL}")
            response = requests.get(Config.HINTERGRUND_URL, timeout=10)
            response.raise_for_status()
            self.background = Image.open(BytesIO(response.content))
            self.background = self.background.resize((Config.WIDTH, Config.HEIGHT), Image.Resampling.LANCZOS)
            logger.info("Hintergrundbild erfolgreich geladen")
        except Exception as e:
            logger.warning(f"Fehler beim Laden des Hintergrundbilds: {e}")
            logger.info("Erstelle Fallback-Hintergrund")
            self.background = self._create_fallback_background()

    def _load_qr_code(self):
        """Lädt oder generiert QR-Code"""
        # Versuche zuerst von URL zu laden
        try:
            logger.info(f"Lade QR-Code von {Config.QR_CODE_URL}")
            response = requests.get(Config.QR_CODE_URL, timeout=10)
            response.raise_for_status()
            self.qr_code = Image.open(BytesIO(response.content))
            self.qr_code = self.qr_code.resize((Config.QR_SIZE, Config.QR_SIZE), Image.Resampling.LANCZOS)
            if self.qr_code.mode != 'RGBA':
                self.qr_code = self.qr_code.convert('RGBA')
            logger.info("QR-Code erfolgreich geladen")
            return
        except Exception as e:
            logger.warning(f"Fehler beim Laden des QR-Codes: {e}")

        # Versuche lokalen QR-Code zu laden
        local_qr_path = Path("assets/QR_news.png")
        if local_qr_path.exists():
            try:
                logger.info(f"Lade lokalen QR-Code von {local_qr_path}")
                self.qr_code = Image.open(local_qr_path)
                self.qr_code = self.qr_code.resize((Config.QR_SIZE, Config.QR_SIZE), Image.Resampling.LANCZOS)
                if self.qr_code.mode != 'RGBA':
                    self.qr_code = self.qr_code.convert('RGBA')
                logger.info("Lokaler QR-Code erfolgreich geladen")
                return
            except Exception as e:
                logger.warning(f"Fehler beim Laden des lokalen QR-Codes: {e}")

        # Generiere QR-Code
        try:
            logger.info("Generiere QR-Code für Gemeinde-Website")
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data('https://gemeinde-konkordia.de')  # URL der Gemeinde-Website
            qr.make(fit=True)

            # Erstelle QR-Code Bild
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.convert('RGBA')
            self.qr_code = qr_img.resize((Config.QR_SIZE, Config.QR_SIZE), Image.Resampling.LANCZOS)

            # Speichere generierten QR-Code für zukünftige Verwendung
            local_qr_path.parent.mkdir(exist_ok=True)
            qr_img.save(local_qr_path, 'PNG')
            logger.info("QR-Code erfolgreich generiert und gespeichert")
        except Exception as e:
            logger.error(f"Fehler beim Generieren des QR-Codes: {e}")
            self.qr_code = None

    def _create_fallback_background(self) -> Image.Image:
        """Erstellt einen einfachen Fallback-Hintergrund"""
        img = Image.new('RGB', (Config.WIDTH, Config.HEIGHT), (40, 40, 50))
        return img

    def _load_fonts(self):
        """Lädt Fonts"""
        font_names = [
            'DejaVuSans-Bold.ttf',
            'DejaVuSans.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'Arial.ttf',
            'Helvetica.ttf',
        ]

        # Versuche verschiedene Font-Größen zu laden
        sizes = [Config.TITLE_FONT_SIZE, Config.TITLE_FONT_SIZE_MIN,
                 Config.DESC_FONT_SIZE, Config.FOOTER_FONT_SIZE, 90, 80, 70, 60, 50, 48, 40, 36]

        for size in sizes:
            for font_name in font_names:
                try:
                    self.fonts[f'bold_{size}'] = ImageFont.truetype(font_name, size)
                    break
                except:
                    continue

            # Fallback zu Default
            if f'bold_{size}' not in self.fonts:
                self.fonts[f'bold_{size}'] = ImageFont.load_default()

        # Regular Font
        regular_fonts = [
            'DejaVuSans.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'Arial.ttf',
        ]

        for size in sizes:
            for font_name in regular_fonts:
                try:
                    self.fonts[f'regular_{size}'] = ImageFont.truetype(font_name, size)
                    break
                except:
                    continue

            if f'regular_{size}' not in self.fonts:
                self.fonts[f'regular_{size}'] = ImageFont.load_default()

    def get_font(self, style: str, size: int) -> ImageFont.FreeTypeFont:
        """Gibt Font zurück"""
        key = f"{style}_{size}"
        return self.fonts.get(key, self.fonts.get(f'{style}_{Config.FOOTER_FONT_SIZE}', ImageFont.load_default()))


class EventParser:
    """Parsed iCal-Events"""

    @staticmethod
    def parse_ical_files(file_paths: List[str]) -> List[Dict]:
        """Parsed alle iCal-Dateien und gibt Events zurück"""
        all_events = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                logger.warning(f"iCal-Datei nicht gefunden: {file_path}")
                continue

            try:
                with open(file_path, 'rb') as f:
                    cal = Calendar.from_ical(f.read())
                    events = EventParser._extract_events(cal)
                    all_events.extend(events)
                    logger.info(f"Gefunden: {len(events)} Events in {file_path}")
            except Exception as e:
                logger.error(f"Fehler beim Parsen von {file_path}: {e}")

        # Sortiere nach Datum
        all_events.sort(key=lambda x: x['dtstart'])

        # Filtere nur Termine der nächsten 14 Tage
        now = datetime.now(Config.TIMEZONE)
        end_date = now + timedelta(days=Config.DAYS_AHEAD)

        filtered_events = [
            e for e in all_events
            if now <= e['dtstart'] <= end_date
        ]

        logger.info(f"Insgesamt {len(filtered_events)} Events in den nächsten {Config.DAYS_AHEAD} Tagen")
        return filtered_events

    @staticmethod
    def _extract_events(cal: Calendar) -> List[Dict]:
        """Extrahiert Events aus Kalender"""
        events = []

        for component in cal.walk():
            if component.name == "VEVENT":
                try:
                    event = EventParser._parse_event(component)
                    if event:
                        events.append(event)
                except Exception as e:
                    logger.warning(f"Fehler beim Parsen eines Events: {e}")

        return events

    @staticmethod
    def _parse_event(component) -> Optional[Dict]:
        """Parsed ein einzelnes Event"""
        try:
            # Extrahiere Daten
            summary = str(component.get('summary', 'Veranstaltung'))
            description = str(component.get('description', ''))
            location = str(component.get('location', ''))

            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt if component.get('dtend') else None

            # Konvertiere zu datetime mit Timezone
            if isinstance(dtstart, datetime):
                if dtstart.tzinfo is None:
                    dtstart = dtstart.replace(tzinfo=Config.TIMEZONE)
                else:
                    dtstart = dtstart.astimezone(Config.TIMEZONE)
            else:
                # Falls nur Datum, setze auf Mitternacht
                dtstart = datetime.combine(dtstart, datetime.min.time()).replace(tzinfo=Config.TIMEZONE)

            if dtend:
                if isinstance(dtend, datetime):
                    if dtend.tzinfo is None:
                        dtend = dtend.replace(tzinfo=Config.TIMEZONE)
                    else:
                        dtend = dtend.astimezone(Config.TIMEZONE)
                else:
                    dtend = datetime.combine(dtend, datetime.min.time()).replace(tzinfo=Config.TIMEZONE)

            return {
                'summary': summary,
                'description': description,
                'location': location,
                'dtstart': dtstart,
                'dtend': dtend
            }
        except Exception as e:
            logger.warning(f"Fehler beim Extrahieren von Event-Daten: {e}")
            return None


class SlideGenerator:
    """Generiert PNG-Folien"""

    def __init__(self, assets: AssetManager):
        self.assets = assets

    def generate_event_slide(self, event: Dict, output_path: str):
        """Generiert eine Event-Folie"""
        logger.info(f"Generiere Folie: {event['summary']}")

        # Erstelle Basis-Bild mit Hintergrund
        img = self.assets.background.copy()

        # Verdunkle Hintergrund leicht
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 80))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)

        draw = ImageDraw.Draw(img)

        # Titel-Banner (roter Banner oben)
        banner_height = self._draw_title_banner(draw, event['summary'])

        # Beschreibung (mittig)
        desc_y = banner_height + 60
        if event['description']:
            desc_y = self._draw_description(draw, event['description'], desc_y)

        # Footer (weißer Footer unten)
        self._draw_footer(img, draw, event)

        # Speichern
        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        logger.info(f"Folie gespeichert: {output_path}")

    def _draw_title_banner(self, draw: ImageDraw.Draw, title: str) -> int:
        """Zeichnet roten Banner mit Titel, gibt Höhe zurück"""
        # Titel in Großbuchstaben
        title = title.upper()

        # Finde passende Font-Größe
        font = self._get_fitting_font(title, Config.TITLE_FONT_SIZE, Config.TITLE_FONT_SIZE_MIN, Config.WIDTH - 2 * Config.BANNER_PADDING)

        # Berechne Text-Höhe
        bbox = draw.textbbox((0, 0), title, font=font)
        text_height = bbox[3] - bbox[1]

        # Banner-Höhe
        banner_height = max(Config.BANNER_HEIGHT_MIN, min(Config.BANNER_HEIGHT_MAX, text_height + 2 * Config.BANNER_PADDING))

        # Zeichne roten Banner
        draw.rectangle(
            [(0, 0), (Config.WIDTH, banner_height)],
            fill=Config.GEMEINDE_ROT
        )

        # Zeichne Titel (zentriert)
        text_y = (banner_height - text_height) // 2
        self._draw_centered_text(draw, title, text_y, font, Config.WEISS)

        return banner_height

    def _draw_description(self, draw: ImageDraw.Draw, description: str, start_y: int) -> int:
        """Zeichnet Beschreibung (max 4 Zeilen), gibt End-Y zurück"""
        # Bereinige Beschreibung
        description = description.replace('\\n', '\n').replace('\\r', '').strip()

        # Font für Beschreibung
        font = self.assets.get_font('regular', Config.DESC_FONT_SIZE)

        # Maximale Breite
        max_width = Config.WIDTH - 200

        # Teile Text in Zeilen
        lines = self._wrap_text(description, font, max_width, draw)

        # Maximal 4 Zeilen
        lines = lines[:4]

        # Zeichne Zeilen
        y = start_y
        line_height = Config.DESC_FONT_SIZE + 15

        for line in lines:
            self._draw_centered_text(draw, line, y, font, Config.WEISS)
            y += line_height

        return y

    def _draw_footer(self, img: Image.Image, draw: ImageDraw.Draw, event: Dict):
        """Zeichnet weißen Footer mit Details und QR-Code (neues Layout)"""
        footer_y = Config.HEIGHT - Config.FOOTER_HEIGHT

        # Hellgrauer Footer-Hintergrund (wie im Screenshot)
        draw.rectangle(
            [(0, footer_y), (Config.WIDTH, Config.HEIGHT)],
            fill=(240, 240, 240)  # Hellgrau statt reinweiß
        )

        # Formatiere Datum und Zeit
        wochentag = Config.WOCHENTAGE[event['dtstart'].weekday()]
        datum = f"{event['dtstart'].day}. {Config.MONATE[event['dtstart'].month]} {event['dtstart'].year}"
        time_str = self._format_time(event['dtstart'], event['dtend'])
        location_str = event['location'] if event['location'] else ''

        # Fonts für verschiedene Größen
        font_wochentag = self.assets.get_font('regular', 38)
        font_datum = self.assets.get_font('bold', 85)  # Großes Datum wie im Screenshot
        font_details = self.assets.get_font('regular', 36)

        # Berechne verfügbare Breite (minus QR-Code Bereich)
        content_width = Config.WIDTH - Config.QR_SIZE - 3 * Config.FOOTER_PADDING

        # Y-Position für zentrierten Content
        y = footer_y + 30

        # 1. Wochentag (zentriert, kleinere Schrift)
        self._draw_left_aligned_text(draw, wochentag, Config.FOOTER_PADDING, y, font_wochentag, Config.SCHWARZ)
        y += 50

        # 2. Datum (zentriert, sehr große Schrift)
        self._draw_left_aligned_text(draw, datum, Config.FOOTER_PADDING, y, font_datum, Config.SCHWARZ)
        y += 95

        # 3. Uhrzeit mit Icon
        if time_str:
            # Unicode Clock Icon
            time_text = f"🕐 {time_str}"
            self._draw_left_aligned_text(draw, time_text, Config.FOOTER_PADDING, y, font_details, Config.SCHWARZ)
            y += 48

        # 4. Ort mit Icon (gekürzt falls zu lang)
        if location_str:
            location_str = self._truncate_text(location_str, font_details, content_width - Config.FOOTER_PADDING, draw)
            location_text = f"📍 {location_str}"
            self._draw_left_aligned_text(draw, location_text, Config.FOOTER_PADDING, y, font_details, Config.SCHWARZ)

        # QR-Code (rechts im Footer, zentriert vertikal)
        if self.assets.qr_code:
            qr_x = Config.WIDTH - Config.QR_SIZE - Config.FOOTER_PADDING
            qr_y = footer_y + (Config.FOOTER_HEIGHT - Config.QR_SIZE) // 2
            img.paste(self.assets.qr_code, (qr_x, qr_y), self.assets.qr_code)

    def _format_date(self, dt: datetime) -> str:
        """Formatiert Datum auf Deutsch"""
        wochentag = Config.WOCHENTAGE[dt.weekday()]
        monat = Config.MONATE[dt.month]
        return f"{wochentag}, {dt.day}. {monat} {dt.year}"

    def _format_time(self, start: datetime, end: Optional[datetime]) -> str:
        """Formatiert Uhrzeit"""
        if not start:
            return ""

        start_str = start.strftime("%H:%M")

        if end and end != start:
            end_str = end.strftime("%H:%M")
            return f"{start_str} - {end_str} Uhr"

        return f"{start_str} Uhr"

    def _get_fitting_font(self, text: str, max_size: int, min_size: int, max_width: int) -> ImageFont.FreeTypeFont:
        """Findet passende Font-Größe für Text"""
        for size in range(max_size, min_size - 1, -10):
            font = self.assets.get_font('bold', size)
            # Teste Breite
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                return font

        return self.assets.get_font('bold', min_size)

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """Teilt Text in Zeilen auf"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _truncate_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> str:
        """Kürzt Text mit ... falls zu lang"""
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            return text

        # Kürze Text
        for i in range(len(text), 0, -1):
            truncated = text[:i] + "..."
            bbox = draw.textbbox((0, 0), truncated, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                return truncated

        return "..."

    def _draw_centered_text(self, draw: ImageDraw.Draw, text: str, y: int, font: ImageFont.FreeTypeFont, color):
        """Zeichnet zentrierten Text"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (Config.WIDTH - text_width) // 2
        draw.text((x, y), text, font=font, fill=color)

    def _draw_left_aligned_text(self, draw: ImageDraw.Draw, text: str, x: int, y: int, font: ImageFont.FreeTypeFont, color):
        """Zeichnet linksbündigen Text"""
        draw.text((x, y), text, font=font, fill=color)

    def generate_title_slide(self, output_path: str):
        """Generiert Titel-Folie"""
        logger.info("Generiere Titel-Folie")

        img = self.assets.background.copy()
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 100))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)

        draw = ImageDraw.Draw(img)

        # Titel
        title = "VERANSTALTUNGEN"
        subtitle = "Gemeinde in der Konkordia"
        date_info = "Nächste 14 Tage"

        font_title = self.assets.get_font('bold', 120)
        font_subtitle = self.assets.get_font('regular', 60)
        font_date = self.assets.get_font('regular', 48)

        # Zentriert
        y = Config.HEIGHT // 3
        self._draw_centered_text(draw, title, y, font_title, Config.WEISS)
        y += 150
        self._draw_centered_text(draw, subtitle, y, font_subtitle, Config.WEISS)
        y += 100
        self._draw_centered_text(draw, date_info, y, font_date, Config.WEISS)

        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        logger.info(f"Titel-Folie gespeichert: {output_path}")


def get_info_slides() -> List[str]:
    """Findet alle Info-Folien im slides/ Ordner"""
    info_slides = []
    slides_dir = Path(Config.INFO_SLIDES_DIR)

    for file in sorted(slides_dir.glob("slide*.jpg")):
        info_slides.append(str(file))

    logger.info(f"Gefunden: {len(info_slides)} Info-Folien")
    return info_slides


def generate_slides():
    """Hauptfunktion: Generiert alle Folien"""
    logger.info("=== Starte Folien-Generierung ===")

    # Assets laden
    assets = AssetManager()

    # Events parsen
    ical_files = Config.ICAL_FILES
    events = EventParser.parse_ical_files(ical_files)

    if not events:
        logger.warning("Keine Events gefunden!")

    # Ausgabe-Verzeichnis erstellen
    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Lösche alte generierte Folien (nur slide_*.png)
    for old_file in output_dir.glob("slide_*.png"):
        old_file.unlink()
        logger.info(f"Gelöscht: {old_file}")

    # Slide Generator
    generator = SlideGenerator(assets)

    # Generiere Folien
    slide_number = 0

    # 1. Titel-Folie
    title_path = output_dir / f"slide_{slide_number:02d}_titel.png"
    generator.generate_title_slide(str(title_path))
    slide_number += 1

    # 2. Info-Folien holen
    info_slides = get_info_slides()
    info_index = 0

    # 3. Event-Folien mit Info-Folien im 3:1 Rhythmus
    for i, event in enumerate(events):
        # Event-Folie
        event_date = event['dtstart'].strftime("%d%b")
        event_name = event['summary'][:20].replace(' ', '_')
        filename = f"slide_{slide_number:02d}_{event_name}_{event_date}.png"
        output_path = output_dir / filename

        generator.generate_event_slide(event, str(output_path))
        slide_number += 1

        # Nach jedem 3. Event eine Info-Folie
        if (i + 1) % 3 == 0 and info_slides:
            # Kopiere Info-Folie (behalte Original)
            info_slide_src = info_slides[info_index % len(info_slides)]
            info_slide_dest = output_dir / f"slide_{slide_number:02d}_info.png"

            # Konvertiere JPG zu PNG
            info_img = Image.open(info_slide_src)
            info_img = info_img.resize((Config.WIDTH, Config.HEIGHT), Image.Resampling.LANCZOS)
            info_img.save(info_slide_dest, 'PNG')

            logger.info(f"Info-Folie kopiert: {info_slide_dest}")
            slide_number += 1
            info_index += 1

    logger.info(f"=== Fertig! {slide_number} Folien generiert ===")
    return slide_number


if __name__ == "__main__":
    try:
        generate_slides()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fehler bei der Generierung: {e}", exc_info=True)
        sys.exit(1)
