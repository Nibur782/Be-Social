"""
Generuje featured images dla 10 artykułów blogowych.
Każda grafika to dedykowana wizualizacja tematu (nie ogólna karta OG),
która ma się wyświetlać w hero artykułu i na karcie w blog.html.

Wymiary: 1200x630 (16:8.4), zapisane jako WebP (~50-80 KB).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

ROOT = Path(__file__).parent
OUT = ROOT / "blog" / "img"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630

# Brand colors
BRAND_BLUE = (29, 78, 216)        # #1D4ED8
BRAND_BLUE_DARK = (15, 23, 42)    # slate-900
BRAND_BLUE_LIGHT = (96, 165, 250) # blue-400
WHITE = (255, 255, 255)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)
SLATE_500 = (100, 116, 139)
SLATE_600 = (71, 85, 105)
SLATE_700 = (51, 65, 85)
SLATE_900 = (15, 23, 42)
GREEN = (34, 197, 94)
GREEN_DARK = (5, 150, 105)
YELLOW = (250, 204, 21)
RED = (239, 68, 68)
PINK = (236, 72, 153)
PURPLE = (168, 85, 247)
AMBER = (217, 119, 6)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"


def f(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def gradient_bg(c1=BRAND_BLUE_DARK, c2=BRAND_BLUE):
    """Diagonal gradient."""
    bg = Image.new("RGB", (W, H), c1)
    px = bg.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.6 + y / H * 0.4)
            r = int(c1[0] * (1 - t) + c2[0] * t * 0.85)
            g = int(c1[1] * (1 - t) + c2[1] * t * 0.85)
            b = int(c1[2] * (1 - t) + c2[2] * t * 0.85)
            px[x, y] = (r, g, b)
    return bg


def add_glow(img, center, radius, color, opacity=0.4):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    for r in range(radius, 0, -8):
        a = int(255 * opacity * (1 - r / radius) ** 2)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (a,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    img.paste(overlay, (0, 0), overlay)
    return img


def draw_label(draw, color=BRAND_BLUE_LIGHT):
    """Górny label brandowy."""
    draw.rectangle((80, 70, 140, 78), fill=color)
    draw.text((80, 95), "DAWIDRUBIN.PL / BLOG", font=f(22), fill=color)


def draw_footer(draw):
    """Stopka brandowa."""
    draw.line((80, H - 80, 200, H - 80), fill=BRAND_BLUE_LIGHT, width=3)
    draw.text((80, H - 60), "Dawid Rubin", font=f(24), fill=WHITE)
    draw.text((80, H - 32), "Konsultant marketingowy · 8+ lat doświadczenia", font=f(18, False), fill=SLATE_300)


def wrap(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


# ============ 1. WIZYTÓWKA GOOGLE ============
def img_wizytowka_google():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (220, 150), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 500), 320, GREEN, 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    # Tytuł - zmniejszony żeby nie nachodził na mockup
    title = "Wizytówka Google"
    draw.text((80, 160), title, font=f(48), fill=WHITE)
    draw.text((80, 215), "krok po kroku", font=f(40), fill=BRAND_BLUE_LIGHT)

    # Mockup wizytówki Google (prawa strona)
    card_x, card_y, card_w, card_h = 720, 160, 400, 360
    # Cień
    shadow = Image.new("RGBA", (card_w + 40, card_h + 40), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle((20, 20, card_w + 20, card_h + 20), radius=20, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    bg.paste(shadow, (card_x - 20, card_y - 20), shadow)
    # Karta
    draw.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h), radius=16, fill=WHITE)
    # Header zdjęcia
    draw.rectangle((card_x, card_y, card_x + card_w, card_y + 120), fill=(220, 235, 255))
    # Logo wewnątrz
    draw.rounded_rectangle((card_x + 20, card_y + 90, card_x + 100, card_y + 170), radius=8, fill=BRAND_BLUE)
    draw.text((card_x + 38, card_y + 117), "PR", font=f(36), fill=WHITE)
    # Nazwa
    draw.text((card_x + 120, card_y + 110), "Pracownia", font=f(22), fill=SLATE_900)
    draw.text((card_x + 120, card_y + 138), "Rachunkowości", font=f(22), fill=SLATE_900)
    # Gwiazdki
    star_y = card_y + 190
    for i in range(5):
        sx = card_x + 24 + i * 32
        # gwiazda jako wielokąt
        cx, cy, r = sx + 12, star_y + 12, 12
        points = []
        for k in range(10):
            ang = math.radians(90 + k * 36)
            radius = r if k % 2 == 0 else r * 0.45
            points.append((cx + radius * math.cos(ang), cy - radius * math.sin(ang)))
        draw.polygon(points, fill=YELLOW)
    draw.text((card_x + 200, star_y + 2), "5.0", font=f(22), fill=SLATE_900)
    draw.text((card_x + 250, star_y + 5), "(127 opinii)", font=f(16, False), fill=SLATE_500)
    # Kategoria
    draw.text((card_x + 24, card_y + 240), "Biuro rachunkowe · Otwarte", font=f(18, False), fill=GREEN_DARK)
    # Adres
    draw.text((card_x + 24, card_y + 272), "ul. Marketingowa 1, Warszawa", font=f(16, False), fill=SLATE_600)
    # Przyciski
    draw.rounded_rectangle((card_x + 24, card_y + 305, card_x + 184, card_y + 340), radius=18, fill=BRAND_BLUE)
    draw.text((card_x + 70, card_y + 313), "Zadzwoń", font=f(16), fill=WHITE)
    draw.rounded_rectangle((card_x + 196, card_y + 305, card_x + 376, card_y + 340), radius=18, outline=BRAND_BLUE, width=2)
    draw.text((card_x + 250, card_y + 313), "Trasa", font=f(16), fill=BRAND_BLUE)

    # Bullet pod tytułem
    draw.text((80, 320), "✓  Weryfikacja, kategorie, opis, atrybuty", font=f(20, False), fill=SLATE_300)
    draw.text((80, 354), "✓  Zdjęcia, opinie, posty, Q&A, produkty", font=f(20, False), fill=SLATE_300)
    draw.text((80, 388), "✓  12 błędów, które kosztują widoczność", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-wizytowka-google.webp", bg)


# ============ 2. META ADVANTAGE+ ============
def img_meta_advantage():
    bg = gradient_bg(BRAND_BLUE_DARK, (24, 119, 242))  # Meta blue
    bg = add_glow(bg, (200, 200), 400, BRAND_BLUE_LIGHT, 0.5)
    bg = add_glow(bg, (1050, 500), 350, (24, 119, 242), 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Meta Advantage+", font=f(56), fill=WHITE)
    draw.text((80, 222), "czy warto w 2026?", font=f(40), fill=BRAND_BLUE_LIGHT)

    # Wykres ROAS w prawym dolnym
    chart_x, chart_y = 670, 200
    chart_w, chart_h = 470, 280
    # Tło wykresu
    draw.rounded_rectangle((chart_x, chart_y, chart_x + chart_w, chart_y + chart_h), radius=14, fill=(255, 255, 255, 240))
    # Gridlines
    for i in range(1, 5):
        y = chart_y + 30 + i * (chart_h - 60) // 5
        draw.line((chart_x + 20, y, chart_x + chart_w - 20, y), fill=(230, 235, 245), width=1)
    # Bar chart - 6 słupków
    bar_w = 50
    gap = 20
    base_x = chart_x + 50
    base_y = chart_y + chart_h - 50
    heights = [110, 95, 140, 130, 180, 220]
    labels = ["W1", "W2", "W3", "W4", "W5", "W6"]
    for i, h_ in enumerate(heights):
        bx = base_x + i * (bar_w + gap)
        # gradient bar
        draw.rounded_rectangle((bx, base_y - h_, bx + bar_w, base_y), radius=6, fill=BRAND_BLUE)
        draw.text((bx + 12, base_y + 12), labels[i], font=f(14, False), fill=SLATE_600)
    # Label nad ostatnim
    draw.text((base_x + 5 * (bar_w + gap) - 10, base_y - 250), "+34%", font=f(24), fill=GREEN_DARK)
    # Tytuł wykresu
    draw.text((chart_x + 20, chart_y + 18), "ROAS po wdrożeniu ADV+", font=f(18), fill=SLATE_700)

    # Bullety
    draw.text((80, 310), "✓  Kiedy ADV+ Shopping wymiata", font=f(20, False), fill=SLATE_300)
    draw.text((80, 344), "✓  Kiedy zabija konto", font=f(20, False), fill=SLATE_300)
    draw.text((80, 378), "✓  Vasco Electronics: 20+ rynków, 100k+ PLN/mies.", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-meta-advantage-plus.webp", bg)


# ============ 3. PERFORMANCE MAX ============
def img_performance_max():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 450), 330, (66, 133, 244), 0.35)  # Google blue
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Performance Max", font=f(58), fill=WHITE)
    draw.text((80, 224), "6 kanałów Google w jednym", font=f(34), fill=BRAND_BLUE_LIGHT)

    # 6 kanałów Google jako kafelki
    channels = [
        ("Search", (66, 133, 244)),
        ("Shopping", (52, 168, 83)),
        ("YouTube", (255, 0, 0)),
        ("Display", (251, 188, 5)),
        ("Discover", (66, 133, 244)),
        ("Gmail", (234, 67, 53)),
    ]
    tile_x, tile_y = 640, 180
    tile_w, tile_h = 220, 75
    gap = 12
    for i, (name, col) in enumerate(channels):
        col_idx = i % 2
        row_idx = i // 2
        x = tile_x + col_idx * (tile_w + gap)
        y = tile_y + row_idx * (tile_h + gap)
        draw.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=12, fill=WHITE)
        # Color dot
        draw.ellipse((x + 16, y + 22, x + 46, y + 52), fill=col)
        draw.text((x + 60, y + 24), name, font=f(22), fill=SLATE_900)
        if i == 1:  # Shopping - badge "50-70%"
            draw.rounded_rectangle((x + tile_w - 70, y + 22, x + tile_w - 14, y + 50), radius=14, fill=(220, 252, 231))
            draw.text((x + tile_w - 63, y + 27), "50-70%", font=f(14), fill=GREEN_DARK)

    # Centralny element - "1 budżet"
    cb_y = tile_y + 3 * (tile_h + gap) + 10
    draw.rounded_rectangle((640, cb_y, 1080, cb_y + 50), radius=12, fill=BRAND_BLUE)
    draw.text((720, cb_y + 14), "→  1 budżet, 1 algorytm AI  ←", font=f(20), fill=WHITE)

    # Bullety
    draw.text((80, 310), "✓  Asset groups + audience signals", font=f(20, False), fill=SLATE_300)
    draw.text((80, 344), "✓  Brand cannibalization - jak nie dać sobie zjeść", font=f(20, False), fill=SLATE_300)
    draw.text((80, 378), "✓  Konfiguracja od zera + Merchant Center", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-performance-max.webp", bg)


# ============ 4. TARGETOWANIE KREACJĄ ============
def img_targetowanie_kreacja():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (250, 250), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1000, 480), 320, PINK, 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Targetowanie", font=f(58), fill=WHITE)
    draw.text((80, 220), "kreacją.", font=f(58), fill=BRAND_BLUE_LIGHT)

    # 3 kreacje pionowe (phone mockups - smartphone aspect)
    phone_x, phone_y = 680, 180
    phone_w, phone_h = 130, 290
    gap = 18
    hooks = [
        ("Problem", "Twój sklep ma\nporzucone koszyki?"),
        ("Social proof", "Ponad 2 000 firm\nkorzysta z..."),
        ("Statystyka", "+3x leadów\ndzięki..."),
    ]
    colors_hook = [(248, 113, 113), (96, 165, 250), (74, 222, 128)]
    for i, ((label, text), col) in enumerate(zip(hooks, colors_hook)):
        x = phone_x + i * (phone_w + gap)
        # Phone outline
        draw.rounded_rectangle((x, phone_y, x + phone_w, phone_y + phone_h), radius=18, fill=SLATE_900, outline=SLATE_700, width=2)
        # Screen
        screen_inset = 6
        draw.rounded_rectangle((x + screen_inset, phone_y + screen_inset, x + phone_w - screen_inset, phone_y + phone_h - screen_inset), radius=14, fill=col)
        # Notch
        draw.rounded_rectangle((x + phone_w // 2 - 18, phone_y + 4, x + phone_w // 2 + 18, phone_y + 18), radius=8, fill=SLATE_900)
        # Label
        draw.rounded_rectangle((x + 14, phone_y + 28, x + phone_w - 14, phone_y + 50), radius=10, fill=(255, 255, 255, 230))
        draw.text((x + 22, phone_y + 30), label, font=f(13), fill=SLATE_900)
        # Hook text (split lines)
        lines = text.split("\n")
        ty = phone_y + 80
        for line in lines:
            tw = draw.textlength(line, font=f(13))
            draw.text((x + (phone_w - tw) / 2, ty), line, font=f(13), fill=WHITE)
            ty += 18
        # Hook rate
        draw.text((x + 28, phone_y + phone_h - 50), "HOOK", font=f(11, False), fill=(255, 255, 255, 200))
        draw.text((x + 25, phone_y + phone_h - 35), f"{38 - i * 4}%", font=f(22), fill=WHITE)

    # Strzałka między kreacjami a target audience
    draw.text((680, 490), "Algorytm sam dobiera audience na podstawie reakcji →", font=f(18, False), fill=BRAND_BLUE_LIGHT)

    # Bullety
    draw.text((80, 320), "✓  Death of cookie targeting", font=f(20, False), fill=SLATE_300)
    draw.text((80, 354), "✓  Hook rate jako KPI nr 1", font=f(20, False), fill=SLATE_300)
    draw.text((80, 388), "✓  Creative testing framework", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-targetowanie-kreacja.webp", bg)


# ============ 5. GOOGLE ADS PRZEŻYTEK? ============
def img_google_ads_przezytek():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 500), 320, AMBER, 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Google Ads", font=f(58), fill=WHITE)
    draw.text((80, 220), "to przeżytek?", font=f(58), fill=AMBER)

    # 2 kolumny porównawcze - "Co umiera" vs "Co rośnie"
    col_x, col_y = 640, 180
    col_w, col_h = 250, 320

    # Lewa kolumna - co umiera (czerwone)
    draw.rounded_rectangle((col_x, col_y, col_x + col_w, col_y + col_h), radius=14, fill=(254, 226, 226))
    draw.rounded_rectangle((col_x, col_y, col_x + col_w, col_y + 50), radius=14, fill=(248, 113, 113))
    draw.text((col_x + 16, col_y + 12), "❌  CO UMIERA", font=f(20), fill=WHITE)
    dying = [
        "Exact match Search",
        "Display bez audience",
        "Brand bid agresywny",
        "Last-click attribution",
    ]
    for i, item in enumerate(dying):
        ty = col_y + 70 + i * 50
        draw.text((col_x + 16, ty), "—", font=f(20), fill=(220, 38, 38))
        draw.text((col_x + 42, ty), item, font=f(18, False), fill=SLATE_900)

    # Prawa kolumna - co rośnie (zielone)
    col2_x = col_x + col_w + 20
    draw.rounded_rectangle((col2_x, col_y, col2_x + col_w, col_y + col_h), radius=14, fill=(220, 252, 231))
    draw.rounded_rectangle((col2_x, col_y, col2_x + col_w, col_y + 50), radius=14, fill=GREEN)
    draw.text((col2_x + 16, col_y + 12), "✓  CO ROŚNIE", font=f(20), fill=WHITE)
    rising = [
        "Performance Max",
        "Demand Gen",
        "AI Max for Search",
        "Data-driven attribution",
    ]
    for i, item in enumerate(rising):
        ty = col_y + 70 + i * 50
        draw.text((col2_x + 16, ty), "+", font=f(20), fill=GREEN_DARK)
        draw.text((col2_x + 42, ty), item, font=f(18, False), fill=SLATE_900)

    # Bullety
    draw.text((80, 320), "✓  AI Overviews vs klasyczny Search", font=f(20, False), fill=SLATE_300)
    draw.text((80, 354), "✓  Mix budżetu na 2026", font=f(20, False), fill=SLATE_300)
    draw.text((80, 388), "✓  Gdzie przesunąć kasę", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-google-ads-przezytek.webp", bg)


# ============ 6. SEO vs GEO ============
def img_seo_vs_geo():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 500), 320, PURPLE, 0.35)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "SEO ", font=f(72), fill=WHITE)
    seo_w = draw.textlength("SEO ", font=f(72))
    draw.text((80 + seo_w, 160), "vs", font=f(40), fill=SLATE_400)
    vs_w = draw.textlength("vs ", font=f(40))
    draw.text((80 + seo_w + vs_w + 10, 160), "GEO", font=f(72), fill=PURPLE)

    draw.text((80, 250), "pozycjonowanie w dobie AI", font=f(28), fill=BRAND_BLUE_LIGHT)

    # Porównanie SERP - lewa (klasyczny Google) vs prawa (AI Overviews)
    # Lewa: lista niebieskich linków
    left_x, left_y = 80, 320
    draw.text((left_x, left_y), "Klasyczny SERP (SEO):", font=f(18), fill=SLATE_400)
    for i in range(3):
        y = left_y + 40 + i * 35
        draw.rounded_rectangle((left_x, y, left_x + 380, y + 28), radius=6, fill=(255, 255, 255, 25))
        draw.text((left_x + 8, y + 4), f"  Link tytuł #{i+1}", font=f(16, False), fill=BRAND_BLUE_LIGHT)

    # Prawa: AI Overview z cytatami
    right_x = 640
    right_y = 180
    draw.rounded_rectangle((right_x, right_y, right_x + 480, right_y + 360), radius=14, fill=WHITE)
    # Header AI Overview
    draw.rounded_rectangle((right_x, right_y, right_x + 480, right_y + 50), radius=14, fill=PURPLE)
    draw.text((right_x + 16, right_y + 12), "✨  AI Overview (GEO)", font=f(20), fill=WHITE)
    # Body
    body_lines = [
        "GEO to dyscyplina optymalizacji",
        "treści pod kątem cytowania przez",
        "generatywne wyszukiwarki AI.",
        "",
        "Źródła:",
    ]
    for i, line in enumerate(body_lines):
        draw.text((right_x + 16, right_y + 70 + i * 26), line, font=f(15, False), fill=SLATE_700)
    # Citations badges
    cit_y = right_y + 240
    citations = ["dawidrubin.pl", "schema.org", "google.com"]
    for i, c in enumerate(citations):
        cw = draw.textlength(c, font=f(13)) + 30
        cx = right_x + 16 + i * (cw + 10)
        col = BRAND_BLUE if i == 0 else SLATE_400
        draw.rounded_rectangle((cx, cit_y, cx + cw, cit_y + 28), radius=14, fill=col)
        draw.text((cx + 15, cit_y + 5), c, font=f(13), fill=WHITE)
    # Highlight dawidrubin.pl
    draw.text((right_x + 16, cit_y + 40), "← Twoja strona zacytowana", font=f(13), fill=GREEN_DARK)

    draw_footer(draw)
    save("featured-seo-vs-geo.webp", bg)


# ============ 7. MINIMALNY BUDŻET ============
def img_minimalny_budzet():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (250, 250), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1000, 480), 320, AMBER, 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Minimalny", font=f(58), fill=WHITE)
    draw.text((80, 222), "budżet reklamowy.", font=f(46), fill=AMBER)

    # Tabela budżetów per platforma
    table_x, table_y = 640, 180
    rows = [
        ("Lokalny biznes", "30-100 PLN/dzień", GREEN),
        ("Mały e-commerce", "150-400 PLN/dzień", BRAND_BLUE_LIGHT),
        ("Średni e-commerce", "500-2000 PLN/dzień", BRAND_BLUE),
        ("Advantage+ / PMax", "5000+ PLN/dzień", AMBER),
        ("B2B SaaS / LinkedIn", "2000-5000 PLN/dzień", PINK),
    ]
    row_h = 60
    for i, (name, budget, col) in enumerate(rows):
        y = table_y + i * (row_h + 8)
        draw.rounded_rectangle((table_x, y, table_x + 480, y + row_h), radius=10, fill=(255, 255, 255, 250))
        # Color bar
        draw.rounded_rectangle((table_x, y, table_x + 8, y + row_h), radius=10, fill=col)
        draw.text((table_x + 24, y + 8), name, font=f(16, False), fill=SLATE_500)
        draw.text((table_x + 24, y + 28), budget, font=f(20), fill=SLATE_900)

    # Wzór
    formula_y = table_y + 5 * (row_h + 8) + 6
    draw.rounded_rectangle((table_x, formula_y, table_x + 480, formula_y + 50), radius=10, fill=BRAND_BLUE_DARK, outline=BRAND_BLUE_LIGHT, width=2)
    draw.text((table_x + 24, formula_y + 14), "Wzór: CPA × liczba konwersji × 1.3", font=f(18), fill=WHITE)

    # Bullety
    draw.text((80, 310), "✓  Konkretne progi per platforma", font=f(20, False), fill=SLATE_300)
    draw.text((80, 344), "✓  Kiedy 50 PLN/dzień ma sens", font=f(20, False), fill=SLATE_300)
    draw.text((80, 378), "✓  5 błędów z wczesnego stadium", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-minimalny-budzet.webp", bg)


# ============ 8. CONVERSIONS API ============
def img_conversions_api():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 480), 320, PINK, 0.3)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Conversions API", font=f(54), fill=WHITE)
    draw.text((80, 220), "+ Server-Side Tracking", font=f(34), fill=BRAND_BLUE_LIGHT)

    # Diagram: Browser → sGTM → 3 platformy
    diag_y = 220
    # Krok 1: Browser (z X = bloki)
    b1_x = 640
    draw.rounded_rectangle((b1_x, diag_y, b1_x + 120, diag_y + 90), radius=10, fill=(248, 113, 113, 220))
    draw.text((b1_x + 28, diag_y + 10), "Browser", font=f(15), fill=WHITE)
    draw.text((b1_x + 38, diag_y + 38), "🚫", font=f(28), fill=WHITE)
    draw.text((b1_x + 22, diag_y + 68), "-30/50%", font=f(11, False), fill=WHITE)

    # Strzałka VS
    draw.text((b1_x + 130, diag_y + 35), "vs", font=f(18), fill=SLATE_400)

    # Krok 2: Server (CAPI)
    b2_x = b1_x + 160
    draw.rounded_rectangle((b2_x, diag_y, b2_x + 120, diag_y + 90), radius=10, fill=GREEN)
    draw.text((b2_x + 30, diag_y + 10), "Server", font=f(15), fill=WHITE)
    draw.text((b2_x + 32, diag_y + 38), "✓ CAPI", font=f(20), fill=WHITE)
    draw.text((b2_x + 32, diag_y + 68), "+15-30%", font=f(11, False), fill=WHITE)

    # Strzałka →
    arr_y = diag_y + 130
    draw.text((b1_x + 130, arr_y), "→", font=f(40), fill=BRAND_BLUE_LIGHT)

    # 3 platformy do których leci CAPI
    plats = [("Meta", (24, 119, 242)), ("Google", (66, 133, 244)), ("TikTok", (0, 0, 0))]
    plat_y = diag_y + 180
    for i, (name, col) in enumerate(plats):
        px = 640 + i * 110
        draw.rounded_rectangle((px, plat_y, px + 100, plat_y + 50), radius=10, fill=WHITE)
        draw.text((px + 8, plat_y + 6), name, font=f(15), fill=col)
        draw.text((px + 8, plat_y + 28), "EMQ ≥ 7", font=f(11, False), fill=SLATE_600)

    # Big metric (mocno pod platformami)
    draw.rounded_rectangle((640, plat_y + 70, 1100, plat_y + 130), radius=10, fill=(220, 252, 231))
    draw.text((660, plat_y + 80), "ROAS +15-30%", font=f(28), fill=GREEN_DARK)
    draw.text((660, plat_y + 112), "po wdrożeniu CAPI z EMQ ≥ 7.0", font=f(13, False), fill=SLATE_700)

    # Bullety
    draw.text((80, 310), "✓  Pełna instrukcja wdrożenia", font=f(20, False), fill=SLATE_300)
    draw.text((80, 344), "✓  EMQ 7+ i deduplikacja", font=f(20, False), fill=SLATE_300)
    draw.text((80, 378), "✓  4 ścieżki wdrożenia (Shopify → custom)", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-conversions-api.webp", bg)


# ============ 9. AI W MARKETINGU ============
def img_ai_marketing():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 480), 320, PURPLE, 0.35)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "AI w marketingu", font=f(58), fill=WHITE)
    draw.text((80, 222), "7 zastosowań ChatGPT", font=f(34), fill=PURPLE)

    # 7 ikon use casów w siatce 3x3 (zostawiamy 2 puste)
    use_cases = [
        ("📝", "Briefy", "kreacji"),
        ("✍️", "Copy", "warianty"),
        ("📊", "Analiza", "feedbacku"),
        ("🎯", "Brand", "voice GPT"),
        ("📈", "Analiza", "GA4 / Meta"),
        ("🔍", "Research", "konkurencji"),
        ("🤖", "Asystent", "zespołu"),
    ]
    grid_x, grid_y = 640, 175
    tile_w, tile_h = 150, 130
    gap = 12
    for i, (icon, line1, line2) in enumerate(use_cases):
        col_idx = i % 3
        row_idx = i // 3
        x = grid_x + col_idx * (tile_w + gap)
        y = grid_y + row_idx * (tile_h + gap)
        draw.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=12, fill=WHITE)
        # Top accent
        draw.rounded_rectangle((x, y, x + tile_w, y + 6), radius=3, fill=PURPLE)
        # Number badge
        draw.ellipse((x + 8, y + 14, x + 36, y + 42), fill=BRAND_BLUE)
        draw.text((x + 17, y + 19), str(i + 1), font=f(15), fill=WHITE)
        # Icon (emoji)
        draw.text((x + tile_w / 2 - 18, y + 14), icon, font=f(36, False), fill=SLATE_700)
        # Text
        tw1 = draw.textlength(line1, font=f(15))
        tw2 = draw.textlength(line2, font=f(15))
        draw.text((x + (tile_w - tw1) / 2, y + 72), line1, font=f(15), fill=SLATE_900)
        draw.text((x + (tile_w - tw2) / 2, y + 92), line2, font=f(15), fill=SLATE_500)

    # Bullety
    draw.text((80, 310), "✓  Konkretne prompty i ramy", font=f(20, False), fill=SLATE_300)
    draw.text((80, 344), "✓  Custom GPTs uczone na danych firmy", font=f(20, False), fill=SLATE_300)
    draw.text((80, 378), "✓  ChatGPT, Claude, Gemini, Perplexity", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-ai-marketing.webp", bg)


# ============ 10. ATRYBUCJA MULTI-TOUCH ============
def img_atrybucja():
    bg = gradient_bg(BRAND_BLUE_DARK, BRAND_BLUE)
    bg = add_glow(bg, (200, 200), 380, BRAND_BLUE_LIGHT, 0.45)
    bg = add_glow(bg, (1050, 500), 320, PINK, 0.35)
    draw = ImageDraw.Draw(bg)
    draw_label(draw)

    draw.text((80, 160), "Atrybucja", font=f(64), fill=WHITE)
    draw.text((80, 230), "multi-touch", font=f(48), fill=PINK)

    # Ścieżka konwersji - 6 styków + konwersja
    path_y = 270
    touches = [
        ("Reels", (228, 64, 95)),
        ("YT Ads", (255, 0, 0)),
        ("IG", (228, 64, 95)),
        ("Blog", (250, 204, 21)),
        ("Search", (66, 133, 244)),
        ("Brand", (34, 197, 94)),
    ]
    base_x = 680
    touch_w = 65
    gap = 8

    for i, (label, col) in enumerate(touches):
        x = base_x + i * (touch_w + gap)
        # Punkt na osi
        draw.ellipse((x + touch_w // 2 - 12, path_y - 12, x + touch_w // 2 + 12, path_y + 12), fill=col)
        draw.ellipse((x + touch_w // 2 - 5, path_y - 5, x + touch_w // 2 + 5, path_y + 5), fill=WHITE)
        # Label
        draw.text((x + 6, path_y + 24), label, font=f(13), fill=WHITE)
        # Linia łącząca
        if i < len(touches) - 1:
            draw.line((x + touch_w // 2 + 12, path_y, x + touch_w + gap + touch_w // 2 - 12, path_y), fill=SLATE_400, width=2)

    # Konwersja - na końcu
    conv_x = base_x + len(touches) * (touch_w + gap) - 20
    draw.rounded_rectangle((conv_x, path_y - 25, conv_x + 100, path_y + 25), radius=24, fill=GREEN)
    draw.text((conv_x + 14, path_y - 11), "✓ ZAKUP", font=f(14), fill=WHITE)

    # Last-click vs DDA
    lc_y = path_y + 110
    # Last-click box
    draw.rounded_rectangle((680, lc_y, 880, lc_y + 90), radius=10, fill=(254, 226, 226))
    draw.text((694, lc_y + 10), "❌  LAST-CLICK", font=f(15), fill=(220, 38, 38))
    draw.text((694, lc_y + 36), "Brand: 100%", font=f(18), fill=SLATE_900)
    draw.text((694, lc_y + 62), "Reszta: 0% (ignorowana!)", font=f(13, False), fill=SLATE_600)

    # DDA box
    draw.rounded_rectangle((900, lc_y, 1100, lc_y + 90), radius=10, fill=(220, 252, 231))
    draw.text((914, lc_y + 10), "✓  DDA (multi-touch)", font=f(15), fill=GREEN_DARK)
    draw.text((914, lc_y + 36), "Każdy styk = wartość", font=f(15), fill=SLATE_900)
    draw.text((914, lc_y + 62), "Realne dane o lejku", font=f(13, False), fill=SLATE_600)

    # Bullety
    draw.text((80, 320), "✓  4-12 styków w średniej ścieżce", font=f(20, False), fill=SLATE_300)
    draw.text((80, 354), "✓  GA4 DDA + MER + geo-lift", font=f(20, False), fill=SLATE_300)
    draw.text((80, 388), "✓  Jak nie wyłączyć kampanii, która sprzedaje", font=f(20, False), fill=SLATE_300)

    draw_footer(draw)
    save("featured-atrybucja-multi-touch.webp", bg)


def save(name, img):
    p = OUT / name
    img.save(p, "WEBP", quality=88, method=6)
    sz = p.stat().st_size / 1024
    print(f"  > {name} ({sz:.1f} KB)")


def main():
    print(f"Generuje 10 featured images do {OUT}/")
    img_wizytowka_google()
    img_meta_advantage()
    img_performance_max()
    img_targetowanie_kreacja()
    img_google_ads_przezytek()
    img_seo_vs_geo()
    img_minimalny_budzet()
    img_conversions_api()
    img_ai_marketing()
    img_atrybucja()
    print("Gotowe.")


if __name__ == "__main__":
    main()
