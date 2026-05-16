"""
Generuje pliki Open Graph (1200x630 JPG) dla wszystkich podstron dawidrubin.pl.

Po co:
- Facebook, LinkedIn, WhatsApp, X/Twitter, iMessage, Slack, Discord
  NIE wspierają WebP w og:image. Wymagają JPG/PNG.
- Standard FB/LinkedIn: 1200x630 (aspect ratio 1.91:1).
- Plik < 300 KB renderuje się szybciej (FB scraper ma timeout ~10s).

Każdy plik to brandowana karta z gradientem, tytułem, podtytułem i marką.
Dla case studies dodatkowo używa istniejących screenshotów jako akcent wizualny.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).parent
OG = ROOT / "og"
OG.mkdir(exist_ok=True)

W, H = 1200, 630

# Brand colors
BRAND_BLUE = (29, 78, 216)        # #1D4ED8
BRAND_BLUE_DARK = (15, 23, 42)    # slate-900
WHITE = (255, 255, 255)
ACCENT = (96, 165, 250)            # blue-400
SLATE_300 = (203, 213, 225)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"
FONT_BLACK = "C:/Windows/Fonts/arialbd.ttf"  # użyjemy bold jako black


def gradient_background():
    """Diagonal gradient od ciemnego slate do brand blue."""
    bg = Image.new("RGB", (W, H), BRAND_BLUE_DARK)
    px = bg.load()
    for y in range(H):
        for x in range(W):
            # diagonal mix
            t = (x / W * 0.55 + y / H * 0.45)
            r = int(BRAND_BLUE_DARK[0] * (1 - t) + BRAND_BLUE[0] * t * 0.85)
            g = int(BRAND_BLUE_DARK[1] * (1 - t) + BRAND_BLUE[1] * t * 0.85)
            b = int(BRAND_BLUE_DARK[2] * (1 - t) + BRAND_BLUE[2] * t * 0.85)
            px[x, y] = (r, g, b)
    return bg


def add_glow(img, center, radius, color, opacity=0.35):
    """Dodaje miękki świetlny akcent."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    for r in range(radius, 0, -8):
        a = int(255 * opacity * (1 - r / radius) ** 2)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    img.paste(overlay, (0, 0), overlay)
    return img


def fit_font(text, max_width, target_size, font_path, min_size=36):
    """Znajdź największy rozmiar fontu, przy którym tekst mieści się w max_width."""
    size = target_size
    while size > min_size:
        font = ImageFont.truetype(font_path, size)
        bbox = font.getbbox(text)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(font_path, min_size)


def wrap_text(text, font, max_width, draw):
    """Łamie tekst do listy linii o szerokości max_width."""
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def render_card(title, subtitle, badge=None, accent_text="DAWIDRUBIN.PL",
                background_image=None, out="og.jpg"):
    """
    Renderuje kartę OG 1200x630 JPG.

    background_image: opcjonalny Path do obrazu, który pójdzie po prawej stronie
                      jako akcent wizualny (np. screenshot case study).
    """
    bg = gradient_background()
    # akcenty świetlne (lewy górny + prawy dolny)
    bg = add_glow(bg, (220, 120), 360, (96, 165, 250), 0.45)
    bg = add_glow(bg, (1100, 580), 320, (37, 99, 235), 0.35)

    # opcjonalny background_image jako prawa kolumna z maską
    if background_image is not None:
        try:
            src = Image.open(background_image).convert("RGB")
            # dopasuj do prawej kolumny ~520x630
            target_w, target_h = 540, H
            # cover crop
            scale = max(target_w / src.width, target_h / src.height)
            new_w, new_h = int(src.width * scale), int(src.height * scale)
            src = src.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - target_w) // 2
            top = (new_h - target_h) // 2
            src = src.crop((left, top, left + target_w, top + target_h))
            # zaokrąglony lewy fade do bg
            mask = Image.new("L", (target_w, target_h), 255)
            mdraw = ImageDraw.Draw(mask)
            for i in range(80):
                a = int(255 * (i / 80))
                mdraw.line([(i, 0), (i, target_h)], fill=a)
            bg.paste(src, (W - target_w, 0), mask)
        except Exception as e:
            print(f"  ! background_image failed: {e}")

    draw = ImageDraw.Draw(bg)

    # accent górny pasek
    draw.rectangle((80, 70, 80 + 60, 78), fill=ACCENT)

    # accent label u góry
    if accent_text:
        font_accent = ImageFont.truetype(FONT_BOLD, 22)
        draw.text((80, 95), accent_text, font=font_accent, fill=ACCENT)

    # badge (opcjonalny, prawy górny róg)
    if badge:
        font_badge = ImageFont.truetype(FONT_BOLD, 24)
        bw = draw.textlength(badge, font=font_badge) + 40
        bh = 48
        bx = W - 80 - bw
        by = 80
        # pill
        draw.rounded_rectangle((bx, by, bx + bw, by + bh), radius=24,
                               outline=WHITE, width=2)
        tx = bx + (bw - draw.textlength(badge, font=font_badge)) / 2
        draw.text((tx, by + 10), badge, font=font_badge, fill=WHITE)

    # tytuł - duży, max 3 linie
    title_max_w = (W - 160) if background_image is None else 680
    font_title = ImageFont.truetype(FONT_BOLD, 72)
    lines = wrap_text(title, font_title, title_max_w, draw)
    # jeśli więcej niż 3 linie, zmniejsz font
    while len(lines) > 3 and font_title.size > 48:
        font_title = ImageFont.truetype(FONT_BOLD, font_title.size - 4)
        lines = wrap_text(title, font_title, title_max_w, draw)

    line_h = font_title.size + 12
    total_h = line_h * len(lines)
    y = 250 - total_h // 2 + 60
    for line in lines:
        draw.text((80, y), line, font=font_title, fill=WHITE)
        y += line_h

    # podtytuł
    if subtitle:
        sub_max_w = title_max_w
        font_sub = ImageFont.truetype(FONT_REG, 28)
        sub_lines = wrap_text(subtitle, font_sub, sub_max_w, draw)
        sub_lines = sub_lines[:3]
        sy = y + 20
        for sl in sub_lines:
            draw.text((80, sy), sl, font=font_sub, fill=SLATE_300)
            sy += 38

    # stopka - separator + meta
    draw.line((80, H - 80, 200, H - 80), fill=ACCENT, width=3)
    font_foot = ImageFont.truetype(FONT_BOLD, 24)
    draw.text((80, H - 60), "Dawid Rubin", font=font_foot, fill=WHITE)
    font_foot_sub = ImageFont.truetype(FONT_REG, 18)
    draw.text((80, H - 32), "Konsultant marketingowy · 8+ lat doświadczenia",
              font=font_foot_sub, fill=SLATE_300)

    out_path = OG / out
    bg.save(out_path, "JPEG", quality=88, optimize=True, progressive=True)
    size_kb = out_path.stat().st_size / 1024
    print(f"  > {out} ({size_kb:.1f} KB)")
    return out_path


# Definicje wszystkich kart OG
CARDS = [
    {
        "out": "og-home.jpg",
        "title": "Marketing dla firm każdej skali",
        "subtitle": "Kampanie reklamowe, strony internetowe, automatyzacje, audyty i strategia. Jeden ekspert — wszystko pod jednym dachem.",
        "accent_text": "DAWIDRUBIN.PL",
        "badge": "8+ lat",
        "background_image": ROOT / "dawid-rubin-portret.webp",
    },
    {
        "out": "og-audyt-paid-media.jpg",
        "title": "Audyt Paid Media w 5 dni",
        "subtitle": "Dogłębna analiza Meta/Google Ads, GA4, GTM i atrybucji. Raport z konkretnymi rekomendacjami.",
        "accent_text": "DAWIDRUBIN.PL / AUDYT",
        "badge": "5 dni",
        "background_image": None,
    },
    {
        "out": "og-metodologia.jpg",
        "title": "Metodologia pracy",
        "subtitle": "Jak prowadzę projekty marketingowe: od briefu po skalowanie. Konkretne etapy, narzędzia i mierniki sukcesu.",
        "accent_text": "DAWIDRUBIN.PL / METODOLOGIA",
        "badge": None,
        "background_image": None,
    },
    {
        "out": "og-brief-audyt.jpg",
        "title": "Brief audytu marketingowego",
        "subtitle": "Wypełnij brief w 5 minut. Otrzymasz wycenę i plan działania w 24 godziny.",
        "accent_text": "DAWIDRUBIN.PL / BRIEF",
        "badge": "24h",
        "background_image": None,
    },
    {
        "out": "og-brief-projekt.jpg",
        "title": "Brief projektu marketingowego",
        "subtitle": "Strona internetowa, kampania, automatyzacja - opowiedz o projekcie, dobiorę najlepszy kierunek.",
        "accent_text": "DAWIDRUBIN.PL / BRIEF",
        "badge": None,
        "background_image": None,
    },
    {
        "out": "og-umow-rozmowe.jpg",
        "title": "Umów bezpłatną rozmowę",
        "subtitle": "15 minut rozmowy o Twoim biznesie. Bez zobowiązań - sprawdzimy, czy mogę pomóc.",
        "accent_text": "DAWIDRUBIN.PL / KONTAKT",
        "badge": "15 min",
        "background_image": None,
    },
    {
        "out": "og-case-pracownia-rachunkowosci.jpg",
        "title": "Pracownia Rachunkowości — pełen ekosystem",
        "subtitle": "Strona, wizytówka Google, kampanie Meta i Google Ads, mentoring AI. Lokalne biuro rachunkowe od zera do online.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "Case",
        "background_image": None,
    },
    {
        "out": "og-case-wkreceni.jpg",
        "title": "Wkręceni w Rowery - sezonowe kampanie",
        "subtitle": "Lokalny biznes rowerowy: kampanie sezonowe, strona, integracje. Pełen ekosystem marketingowy.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "Case",
        "background_image": ROOT / "screenshots" / "wkreceni-strona.webp",
    },
    {
        "out": "og-case-dietologicznie.jpg",
        "title": "Dietologicznie.pl - pełen ekosystem",
        "subtitle": "Strona, integracje (Stripe, ZnanyLekarz), kampanie i automatyzacje. Zbudowane od zera.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "Case",
        "background_image": ROOT / "screenshots" / "dieto-strona.webp",
    },
    {
        "out": "og-case-globalny-wzrost.jpg",
        "title": "Globalny wzrost sprzedaży +64%",
        "subtitle": "Vasco Electronics - 27 rynków, koordynacja kampanii, zarządzanie budżetem 100k+ PLN/mies.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "+64%",
        "background_image": ROOT / "screenshots" / "vasco-global-results.webp",
    },
    {
        "out": "og-case-automatyzacja.jpg",
        "title": "Automatyzacja - 80% oszczędność czasu",
        "subtitle": "Make + Smartly.io + Google Apps Script: eliminacja powtarzalnej pracy w zespole performance.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "80%",
        "background_image": ROOT / "screenshots" / "vasco-smartly-automation.webp",
    },
    {
        "out": "og-case-vasco-usa.jpg",
        "title": "Wzrost sprzedaży USA +466%",
        "subtitle": "Pivot strategiczny rynku amerykańskiego: nowa segmentacja, atrybucja, struktura kont Meta i Google.",
        "accent_text": "DAWIDRUBIN.PL / CASE STUDY",
        "badge": "+466%",
        "background_image": ROOT / "screenshots" / "vasco-usa-466.webp",
    },
]


def main():
    print(f"Generuje {len(CARDS)} kart OG do {OG}/")
    for card in CARDS:
        render_card(**card)
    print("Gotowe.")


if __name__ == "__main__":
    main()
