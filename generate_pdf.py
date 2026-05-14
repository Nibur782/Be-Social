# -*- coding: utf-8 -*-
"""
Generator PDF: Audyt Paid Media - Checklista 30 punktów
Autor: Dawid Rubin
Format: A4
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, NextPageTemplate
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Brand colors (z audyt-paid-media.html)
BLUE = colors.HexColor("#1D4ED8")
BLUE_DARK = colors.HexColor("#1E3A8A")
BLUE_LIGHT = colors.HexColor("#EFF6FF")
SLATE_900 = colors.HexColor("#0F172A")
SLATE_700 = colors.HexColor("#334155")
SLATE_600 = colors.HexColor("#475569")
SLATE_400 = colors.HexColor("#94A3B8")
SLATE_200 = colors.HexColor("#E2E8F0")
SLATE_100 = colors.HexColor("#F1F5F9")
SLATE_50 = colors.HexColor("#F8FAFC")
RED = colors.HexColor("#DC2626")
AMBER = colors.HexColor("#D97706")
GREEN = colors.HexColor("#059669")

# Rejestracja fontu z polskimi znakami: Calibri (modern, sans-serif, pasuje do brand strony)
FONT_NAME = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

try:
    windir = os.environ.get("WINDIR", r"C:\Windows")
    fonts_dir = os.path.join(windir, "Fonts")
    candidates = [
        ("Calibri", "calibri.ttf", "calibrib.ttf", "calibrii.ttf"),
        ("Arial", "arial.ttf", "arialbd.ttf", "ariali.ttf"),
        ("Segoe", "segoeui.ttf", "segoeuib.ttf", "segoeuii.ttf"),
    ]
    for name, reg, bold, ital in candidates:
        p_reg = os.path.join(fonts_dir, reg)
        p_bold = os.path.join(fonts_dir, bold)
        p_ital = os.path.join(fonts_dir, ital)
        if os.path.exists(p_reg) and os.path.exists(p_bold):
            pdfmetrics.registerFont(TTFont("PLFont", p_reg))
            pdfmetrics.registerFont(TTFont("PLFont-Bold", p_bold))
            FONT_NAME = "PLFont"
            FONT_BOLD = "PLFont-Bold"
            if os.path.exists(p_ital):
                pdfmetrics.registerFont(TTFont("PLFont-Italic", p_ital))
                FONT_ITALIC = "PLFont-Italic"
            break
except Exception:
    pass


CATEGORIES = [
    {
        "name": "Tracking & Analityka",
        "range": "Punkty 1-8",
        "intro": "Bez czystych danych każda decyzja to zgadywanie. Ta sekcja sprawdza fundament – czy w ogóle wiesz, co się dzieje w Twoich kampaniach.",
        "items": [
            {
                "n": 1,
                "title": "GA4 skonfigurowany przez GTM",
                "why": "Bez GTM każda zmiana w trackingu wymaga developera. To blokuje optymalizacje i wydłuża cykl uczenia kampanii.",
                "check": "Sprawdź, czy wszystkie zdarzenia (purchase, ATC, sign_up, lead) są wysyłane przez GTM, a nie hardkodowane w motywie sklepu. Przetestuj zdarzenia w GTM Preview.",
                "priority": "P1",
            },
            {
                "n": 2,
                "title": "Śledzenie e-commerce (ATC, purchase, checkout)",
                "why": "Bez pełnego lejka GA4 i Meta nie mają sygnału do optymalizacji. Konwersje z ostatniego kroku to za mało.",
                "check": "GA4 → Realtime: wykonaj zakup testowy. Sprawdź, czy view_item, add_to_cart, begin_checkout i purchase pojawiają się z pełnymi parametrami (value, currency, items).",
                "priority": "P1",
            },
            {
                "n": 3,
                "title": "Conversions API wdrożone",
                "why": "Po iOS 14.5 pixel browser-side traci 30–50% sygnału. CAPI uzupełnia luki i poprawia jakość atrybucji o 15–30%.",
                "check": "Events Manager Meta → zakładka Overview: sprawdź Event Match Quality. Powinno być ≥ 7.0 dla purchase. Sprawdź, czy zdarzenia mają status „Server” lub „Browser + Server”.",
                "priority": "P1",
            },
            {
                "n": 4,
                "title": "Server-Side Tracking pokrywa 80%+ zdarzeń",
                "why": "Im więcej zdarzeń leci server-side, tym mniej tracisz na adblockerach, ITP i ETP. Pokrycie poniżej 80% to czerwona flaga.",
                "check": "W Events Manager: kolumna „Server” przy zdarzeniach kluczowych. Porównaj liczby z GA4 – serwer powinien łączyć 70–90% wiadomości klienckich.",
                "priority": "P2",
            },
            {
                "n": 5,
                "title": "Zdarzenia iOS14 priorytetyzowane",
                "why": "Meta używa tylko 8 priorytetowych zdarzeń dla użytkowników iOS po ATT. Złe uszeregowanie = stracone konwersje na iOS.",
                "check": "Events Manager → Aggregated Event Measurement: ułożenie zdarzeń od najważniejszego (purchase) do najmniej istotnego. Limit: 8 zdarzeń na domenę.",
                "priority": "P2",
            },
            {
                "n": 6,
                "title": "Deduplikacja browser + server",
                "why": "Bez event_id ta sama konwersja może być zliczona dwa razy (pixel + CAPI). To zafałszowuje ROAS i sztucznie zaniża CPA.",
                "check": "Events Manager → Diagnostics: poszukaj ostrzeżenia „Duplicate events”. Każde zdarzenie CAPI musi mieć ten sam event_id co pixel.",
                "priority": "P1",
            },
            {
                "n": 7,
                "title": "UTM we wszystkich linkach reklamowych",
                "why": "Bez UTM GA4 nie wie, która kampania przyniosła ruch. Tracisz możliwość analizy cross-platform i atrybucji multi-touch.",
                "check": "GA4 → Acquisition → Traffic acquisition: szukaj „not set”, „direct/none” lub „(other)”. Wszystkie kampanie Meta/Google muszą mieć utm_source, utm_medium, utm_campaign.",
                "priority": "P2",
            },
            {
                "n": 8,
                "title": "Ruch wewnętrzny odfiltrowany z GA4",
                "why": "Ruch z biura, agencji i developmentu zafałszowuje konwersje i bounce rate. Bez filtra widzisz dane skażone własnymi sesjami.",
                "check": "GA4 → Admin → Data Streams → Configure tag settings → Define internal traffic. Dodaj IP biura, agencji i developerów. Włącz filtr „Internal” w Data Filters.",
                "priority": "P3",
            },
        ],
    },
    {
        "name": "Architektura kampanii",
        "range": "Punkty 9-15",
        "intro": "Źle ustawiona struktura konta to ciche wyciekanie budżetu. Ta sekcja sprawdza, czy Twoje kampanie nie kanibalizują się nawzajem.",
        "items": [
            {
                "n": 9,
                "title": "Spójna nomenklatura kampanii / Ad Set / Ad",
                "why": "Bez nazw typu [Kraj]_[Cel]_[Audience]_[Format] po 3 miesiącach nikt nie wie, co jest czym. To blokuje raportowanie i analizę per audience.",
                "check": "Otwórz Ads Manager i sprawdź, czy potrafisz w 5 sekund powiedzieć, co każda kampania robi tylko na podstawie nazwy. Jeśli nie – przepisz nazwy.",
                "priority": "P2",
            },
            {
                "n": 10,
                "title": "Zimna i retargetingowa w osobnych kampaniach",
                "why": "Mieszanie ruchu zimnego i retargetingu w jednej kampanii zafałszowuje CPA i utrudnia decyzje budżetowe. To są dwa różne lejki z innymi KPI.",
                "check": "Czy masz osobne kampanie dla TOFU (cold) i BOFU (retargeting/lookalike)? Czy budżet śledzisz osobno dla każdej grupy?",
                "priority": "P1",
            },
            {
                "n": 11,
                "title": "Testy A/B – struktura vs. kreacja osobno",
                "why": "Testowanie kilku zmiennych naraz (audience + kreacja + bid) sprawia, że nie wiesz, co właściwie zadziałało. To jest „testowanie” tylko z nazwy.",
                "check": "Sprawdź ostatnie 3 testy A/B. Czy w każdym była zmieniona TYLKO jedna zmienna? Czy miał jasną hipotezę i kryterium sukcesu?",
                "priority": "P3",
            },
            {
                "n": 12,
                "title": "Optymalizacja pod właściwe zdarzenie (sygnał wraca)",
                "why": "Optymalizacja pod ATC w sklepie z długim cyklem zakupu zwabia tanich klikaczy, nie kupujących. Pixel uczy się złego sygnału.",
                "check": "Każda kampania: czy event optymalizacyjny generuje min. 50 konwersji/tydzień per Ad Set? Jeśli nie – przejdź wyżej w lejek (z purchase na ATC).",
                "priority": "P1",
            },
            {
                "n": 13,
                "title": "Wykluczenia audience między kampaniami",
                "why": "Bez wykluczeń kampania retargetingowa licytuje się z kampanią zimną o tych samych ludzi. Sztucznie podbija CPM i CPA.",
                "check": "Ads Manager → Audiences: czy „website visitors 30d” jest wykluczone z kampanii zimnej? Czy „purchasers 180d” jest wykluczone z retargetingu?",
                "priority": "P2",
            },
            {
                "n": 14,
                "title": "Frequency cap dla retargetingu",
                "why": "Bez capa ten sam użytkownik widzi reklamę 15+ razy w tygodniu. Efekt: ad fatigue, wzrost CPM, spadek CTR, złe skojarzenia z marką.",
                "check": "Reach & frequency w Ads Manager: sprawdź frequency dla retargetingu. Powinno być 3–5/tydzień max. Powyżej tego – dołożyć cap lub odświeżyć kreacje.",
                "priority": "P2",
            },
            {
                "n": 15,
                "title": "CBO vs ABO – świadoma decyzja z uzasadnieniem",
                "why": "Wybór „CBO bo Meta tak mówi” lub „ABO bo zawsze tak robiliśmy” to nie strategia. Każdy etap kampanii wymaga innej decyzji.",
                "check": "Dla każdej kampanii: czy potrafisz w 2 zdaniach uzasadnić, dlaczego CBO/ABO? Jeśli nie – przemyśl. Reguły: CBO dla stabilnych kampanii, ABO dla testów audience.",
                "priority": "P3",
            },
        ],
    },
    {
        "name": "Kreacja i komunikacja",
        "range": "Punkty 16-20",
        "intro": "Po targetingu i bid strategy 80% wyniku robi kreacja. Ta sekcja sprawdza, czy traktujesz kreacje jak najważniejszą zmienną – czy jak dodatek.",
        "items": [
            {
                "n": 16,
                "title": "Min. 3-5 kreacji na Ad Set testowanych równolegle",
                "why": "Jedna kreacja = brak danych do decyzji. Algorytm Meta potrzebuje 3–5 wariantów, żeby zacząć efektywnie wybierać zwycięzcę.",
                "check": "Otwórz aktywne Ad Sety. Ile ma mniej niż 3 aktywne kreacje? Te wymagają interwencji. Czy testujesz różne hooki, formaty, propozycje wartości?",
                "priority": "P1",
            },
            {
                "n": 17,
                "title": "Hook (pierwsze 3 sek.) przetestowany na metrykach",
                "why": "84% użytkowników ocenia, czy ogląda reklamę w pierwszych 3 sekundach. Słaby hook = stracony budżet na zasięgu, który nigdy nie zobaczy oferty.",
                "check": "Ads Manager → Performance breakdown → Video metrics: sprawdź „3-second video views / impressions”. Powinno być > 30%. Jeśli niżej – przepisz hooki.",
                "priority": "P2",
            },
            {
                "n": 18,
                "title": "Kreacje dopasowane do formatu (feed / stories / reels)",
                "why": "Reklama 1:1 wpychana w Stories (9:16) ma czarne paski i wygląda amatorsko. To natychmiastowy „pomiń”. Tracisz na zasięgu bez wartości.",
                "check": "Asset Customization w Ads Managerze: czy masz osobne assety 1:1 (feed), 9:16 (stories/reels), 4:5 (newsfeed mobile)? Lub Advantage+ Placements z dedykowanymi cropami.",
                "priority": "P2",
            },
            {
                "n": 19,
                "title": "Social proof w komunikacji (liczby, opinie, certyfikaty)",
                "why": "Reklama bez dowodu społecznego to obietnica bez gwarancji. Statystyki, opinie i logotypy podnoszą CTR o 20–40% bez zmiany targetingu.",
                "check": "Otwórz top 10 kreacji w ostatnich 90 dniach. Ile ma element social proof? Jeśli mniej niż 5 – to obszar do poprawy.",
                "priority": "P3",
            },
            {
                "n": 20,
                "title": "Lokalizacja kreacji per rynek (język, waluta, kontekst)",
                "why": "Reklama PL z „PLN” wyświetlana w Niemczech to gwarantowany brak konwersji. Tłumaczenie automatyczne to za mało – potrzebny kontekst kulturowy.",
                "check": "Dla każdego rynku: czy masz osobne kreacje w lokalnym języku, z lokalną walutą i lokalnymi referencjami (święta, znane marki, sezony)?",
                "priority": "P2",
            },
        ],
    },
    {
        "name": "Budżet i optymalizacja",
        "range": "Punkty 21-25",
        "intro": "Najczęstsze błędy budżetowe to za szybkie skalowanie i bid strategy ustawiona „na domyślnym”. Ta sekcja sprawdza dyscyplinę operacyjną.",
        "items": [
            {
                "n": 21,
                "title": "Rozkład TOFU/MOFU/BOFU odpowiedni do etapu wzrostu",
                "why": "Sklep w fazie wzrostu z 90% budżetu w retargetingu nie skaluje się – wyczerpie audience. Sklep dojrzały z 90% w cold marnuje budżet na ludzi, którzy już kupili.",
                "check": "Jaka część budżetu idzie w TOFU vs BOFU? Faza startu: 70–80% TOFU. Faza skalowania: 50–60% TOFU. Faza dojrzała: 40–50% TOFU.",
                "priority": "P2",
            },
            {
                "n": 22,
                "title": "Bid strategy dopasowana do celu kampanii",
                "why": "Lowest cost dla zimnej kampanii może obniżyć CPA, ale obniża też jakość audience. Cost cap daje przewidywalność, ale wymaga danych historycznych.",
                "check": "Dla każdej kampanii: czy bid strategy została wybrana świadomie? Lowest cost – na start. Cost cap – po 30+ konwersjach. Bid cap – tylko przy ROAS-cel sztywno ustalony.",
                "priority": "P3",
            },
            {
                "n": 23,
                "title": "Analiza performance per audience (nie tylko kampania)",
                "why": "Średnia ROAS kampanii 3.5 brzmi dobrze, ale może ukrywać: lookalike 1% (ROAS 6.0) i lookalike 5% (ROAS 1.2). Bez breakdownu tracisz najlepsze segmenty.",
                "check": "Ads Manager → Breakdown → by audience/age/gender/placement: czy w ostatnim raporcie analizujesz performance per audience, nie tylko per kampania?",
                "priority": "P2",
            },
            {
                "n": 24,
                "title": "Min. 50 zdarzeń/tydzień per Ad Set (Learning Phase)",
                "why": "Bez 50 konwersji/tydz. Meta nigdy nie wyjdzie z Learning Phase. CPA jest niestabilne, decyzje na tych danych są losowe.",
                "check": "Ads Manager → Delivery: czy widnieje „Learning” lub „Learning limited”? Jeśli tak – konsoliduj Ad Sety albo podnieś budżet, by uzyskać 50 konwersji/tyg.",
                "priority": "P1",
            },
            {
                "n": 25,
                "title": "Skalowanie max. +20% tygodniowo dla stabilnych kampanii",
                "why": "Podwojenie budżetu z dnia na dzień resetuje uczenie kampanii. Algorytm znowu zaczyna od zera, CPA rośnie o 30–50% na 7–14 dni.",
                "check": "Sprawdź historię zmian budżetu w Ads Manager (View Setup History). Czy w ostatnim miesiącu były skoki budżetu > +25%? Jeśli tak – założyć dzienny limit zmiany.",
                "priority": "P2",
            },
        ],
    },
    {
        "name": "Raportowanie",
        "range": "Punkty 26-30",
        "intro": "Raport, którego nikt nie czyta i z którego nikt nie wyciąga wniosków, nie jest raportem. Ta sekcja sprawdza, czy dane prowadzą do decyzji.",
        "items": [
            {
                "n": 26,
                "title": "Dashboard live łączący platformy + GA4",
                "why": "Ręcznie ściągane dane z 5 platform raz w tygodniu to opóźniona reakcja na problem. Anomalia kosztowa na poniedziałek odkryta w piątek to 5 dni zmarnowanego budżetu.",
                "check": "Czy masz Looker Studio / Power BI / Supermetrics dashboard ładujący automatycznie z Meta Ads, Google Ads, GA4, TikTok? Czy odświeża się codziennie?",
                "priority": "P2",
            },
            {
                "n": 27,
                "title": "Atrybucja omawiana jawnie (last-click vs. data-driven)",
                "why": "Last-click niedoszacowuje TOFU (uznaje tylko ostatni touch). Data-driven jest dokładniejsze, ale wymaga 600+ konwersji/mies. Ukryte założenie modelu = złe decyzje.",
                "check": "GA4 → Advertising → Attribution → Model comparison: porównaj last-click i data-driven dla kampanii. Czy znasz różnice? Czy raportujesz wybór jawnie?",
                "priority": "P3",
            },
            {
                "n": 28,
                "title": "Raport tygodniowy z wnioskami (nie tylko danymi)",
                "why": "Raport ze średnimi i wykresami bez „co z tego wynika” nie służy nikomu. Klient nie wie, co robić. Zespół nie wie, co poprawiać.",
                "check": "Otwórz ostatni raport. Czy zawiera sekcje: „co zadziałało”, „co nie zadziałało”, „co zmieniamy w przyszłym tygodniu”? Jeśli nie – dodaj.",
                "priority": "P2",
            },
            {
                "n": 29,
                "title": "Benchmarki branżowe jako punkt odniesienia",
                "why": "CPA 80 PLN to dużo czy mało? Bez benchmarku branżowego (np. Meta Industry Report) nie wiesz. Decyzje budżetowe na „czuję, że jest drogo” to ruletka.",
                "check": "Czy znasz median CPA, ROAS i CPM dla swojej branży? Źródła: Meta Industry Benchmarks, WordStream, Statista, raporty agencji.",
                "priority": "P3",
            },
            {
                "n": 30,
                "title": "Alerty dla anomalii kosztowych (ROAS/CPA progi)",
                "why": "Bez alertów zauważysz problem dopiero przy następnym raporcie – po dniach przepalonego budżetu. Anomalia kosztowa nieobsłużona przez 48h to lekko 5–15% miesięcznego budżetu.",
                "check": "Czy masz skonfigurowane alerty (email/Slack) dla: ROAS < X, CPA > Y, wydatki dzienne > Z? Czy beneficjent alertu ma jasne procedury reakcji?",
                "priority": "P1",
            },
        ],
    },
]


def priority_color(p):
    return {"P1": RED, "P2": AMBER, "P3": GREEN}.get(p, SLATE_400)


# Header/footer na kazdej stronie content
def draw_page_decorations(canvas_obj, doc):
    canvas_obj.saveState()
    page_num = canvas_obj.getPageNumber()

    # Top accent bar
    canvas_obj.setFillColor(BLUE)
    canvas_obj.rect(0, A4[1] - 4 * mm, A4[0], 4 * mm, fill=1, stroke=0)

    # Footer
    if page_num > 1:
        canvas_obj.setFillColor(SLATE_400)
        canvas_obj.setFont(FONT_NAME, 8)
        canvas_obj.drawString(15 * mm, 10 * mm, "Audyt Paid Media – Checklista 30 punktów | Dawid Rubin")
        canvas_obj.drawRightString(A4[0] - 15 * mm, 10 * mm, "Strona %d" % page_num)

        canvas_obj.setStrokeColor(SLATE_200)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(15 * mm, 14 * mm, A4[0] - 15 * mm, 14 * mm)

    canvas_obj.restoreState()


def draw_cover(canvas_obj, doc):
    canvas_obj.saveState()

    # Tlo
    canvas_obj.setFillColor(SLATE_900)
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    # Niebieski pasek
    canvas_obj.setFillColor(BLUE)
    canvas_obj.rect(0, A4[1] - 120 * mm, A4[0], 6 * mm, fill=1, stroke=0)

    # Logo
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont(FONT_BOLD, 16)
    canvas_obj.drawString(20 * mm, A4[1] - 25 * mm, "DAWID")
    canvas_obj.setFillColor(BLUE)
    canvas_obj.drawString(20 * mm + canvas_obj.stringWidth("DAWID", FONT_BOLD, 16), A4[1] - 25 * mm, "RUBIN")

    # Tag
    canvas_obj.setFillColor(BLUE)
    canvas_obj.setFont(FONT_BOLD, 9)
    canvas_obj.drawString(20 * mm, A4[1] - 70 * mm, "DARMOWA CHECKLISTA · 2026")

    # Tytul glowny
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont(FONT_BOLD, 38)
    canvas_obj.drawString(20 * mm, A4[1] - 88 * mm, "Audyt Paid Media")

    canvas_obj.setFillColor(BLUE)
    canvas_obj.setFont(FONT_BOLD, 38)
    canvas_obj.drawString(20 * mm, A4[1] - 103 * mm, "30 punktów.")
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawString(20 * mm + canvas_obj.stringWidth("30 punktów.", FONT_BOLD, 38) + 6 * mm,
                          A4[1] - 103 * mm, "5 kategorii.")

    # Podtytul
    canvas_obj.setFillColor(SLATE_400)
    canvas_obj.setFont(FONT_NAME, 13)
    canvas_obj.drawString(20 * mm, A4[1] - 135 * mm, "Konkretne pytania kontrolne dla e-commerce.")
    canvas_obj.drawString(20 * mm, A4[1] - 143 * mm, "Sprawdź, gdzie przepalasz budżet reklamowy.")

    # Box: co dostajesz
    y = 60 * mm
    canvas_obj.setFillColor(colors.HexColor("#1E3A8A"))
    canvas_obj.roundRect(20 * mm, y, A4[0] - 40 * mm, 50 * mm, 6 * mm, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor("#93C5FD"))
    canvas_obj.setFont(FONT_BOLD, 8)
    canvas_obj.drawString(28 * mm, y + 40 * mm, "CO ZNAJDZIESZ W TYM PDF")

    items = [
        "30 punktów z wyjaśnieniem, dlaczego ma znaczenie i co sprawdzić",
        "Kolumna „Status” do odhaczenia podczas wewnętrznego audytu",
        "Priorytetyzacja P1 / P2 / P3 – od czego zacząć",
        "Konkretne miejsca do sprawdzenia w Ads Manager / GA4 / Events Manager",
    ]
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont(FONT_NAME, 10)
    for i, it in enumerate(items):
        canvas_obj.setFillColor(BLUE)
        canvas_obj.circle(30 * mm, y + 32 * mm - i * 6.5 * mm, 1.5 * mm, fill=1, stroke=0)
        canvas_obj.setFillColor(colors.white)
        canvas_obj.drawString(34 * mm, y + 31 * mm - i * 6.5 * mm, it)

    # Stopka okladki
    canvas_obj.setFillColor(SLATE_400)
    canvas_obj.setFont(FONT_NAME, 8)
    canvas_obj.drawString(20 * mm, 20 * mm, "Dawid Rubin – Architekt Wzrostu | Strategiczny Partner Meta")
    canvas_obj.drawString(20 * mm, 14 * mm, "8+ lat w e-commerce | 20+ rynków | Vasco Electronics, Biedronka, Domodi")

    canvas_obj.restoreState()


def make_pdf(output_path):
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Audyt Paid Media – Checklista 30 punktów",
        author="Dawid Rubin",
        subject="Darmowa checklista audytu Paid Media dla e-commerce",
    )

    cover_frame = Frame(0, 0, A4[0], A4[1], id="cover", showBoundary=0)
    content_frame = Frame(15 * mm, 18 * mm, A4[0] - 30 * mm, A4[1] - 36 * mm, id="content", showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="Content", frames=[content_frame], onPage=draw_page_decorations),
    ])

    styles = getSampleStyleSheet()
    style_h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName=FONT_BOLD,
                              fontSize=22, textColor=SLATE_900, spaceAfter=4, leading=26)
    style_kicker = ParagraphStyle("kicker", parent=styles["Normal"], fontName=FONT_BOLD,
                                  fontSize=9, textColor=BLUE, spaceAfter=4)
    style_intro = ParagraphStyle("intro", parent=styles["Normal"], fontName=FONT_NAME,
                                 fontSize=10.5, textColor=SLATE_600, leading=15, spaceAfter=14)
    style_body = ParagraphStyle("body", parent=styles["Normal"], fontName=FONT_NAME,
                                fontSize=10, textColor=SLATE_700, leading=14, spaceAfter=8)
    style_item_title = ParagraphStyle("itemTitle", parent=styles["Normal"], fontName=FONT_BOLD,
                                      fontSize=12, textColor=SLATE_900, leading=15, spaceAfter=4)
    style_item_body = ParagraphStyle("itemBody", parent=styles["Normal"], fontName=FONT_NAME,
                                     fontSize=9.5, textColor=SLATE_700, leading=13, spaceAfter=2)
    style_prio = ParagraphStyle("prio", parent=styles["Normal"], fontName=FONT_BOLD,
                                fontSize=8, textColor=colors.white, alignment=TA_CENTER, leading=10)
    style_section_label = ParagraphStyle("sectionLabel", parent=styles["Normal"], fontName=FONT_BOLD,
                                         fontSize=9, textColor=BLUE, spaceAfter=4)
    style_section_title = ParagraphStyle("sectionTitle", parent=styles["Heading1"], fontName=FONT_BOLD,
                                         fontSize=20, textColor=SLATE_900, spaceAfter=6, leading=24)
    style_section_intro = ParagraphStyle("sectionIntro", parent=styles["Normal"], fontName=FONT_ITALIC,
                                         fontSize=10, textColor=SLATE_600, leading=14, spaceAfter=14)
    style_centered_h2 = ParagraphStyle("centeredH2", parent=styles["Heading2"], fontName=FONT_BOLD,
                                       fontSize=18, textColor=SLATE_900, alignment=TA_CENTER, leading=22, spaceAfter=8)
    style_centered_body = ParagraphStyle("centeredBody", parent=styles["Normal"], fontName=FONT_NAME,
                                         fontSize=10.5, textColor=SLATE_600, alignment=TA_CENTER, leading=15, spaceAfter=12)

    story = []

    # === COVER ===
    story.append(NextPageTemplate("Content"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # === STRONA: Jak korzystac z checklisty ===
    story.append(Paragraph("INSTRUKCJA", style_kicker))
    story.append(Paragraph("Jak korzystać z tej checklisty", style_h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Checklista zawiera 30 konkretnych pytań kontrolnych pogrupowanych w 5 kategorii. "
        "Każde pytanie ma trzy elementy: <b>dlaczego ma znaczenie</b>, <b>co sprawdzić</b> i "
        "<b>priorytet</b> (P1/P2/P3). Po prawej stronie masz kolumnę Status do odhaczenia.",
        style_intro
    ))

    # Legenda priorytetow
    leg_data = [
        [
            Paragraph("<b>P1</b>", style_prio),
            Paragraph("<b>Naprawić najpierw</b>", style_body),
            Paragraph("Brak tego punktu znacząco zafałszowuje dane, kanibalizuje budżet lub blokuje skalowanie. Krytyczne dla każdej kampanii e-commerce.", style_body),
        ],
        [
            Paragraph("<b>P2</b>", style_prio),
            Paragraph("<b>Ważne</b>", style_body),
            Paragraph("Brak generuje straty 5–15% budżetu lub blokuje skuteczną optymalizację. Naprawić w ciągu 1–2 tygodni od audytu.", style_body),
        ],
        [
            Paragraph("<b>P3</b>", style_prio),
            Paragraph("<b>Optymalizacja</b>", style_body),
            Paragraph("Doprecyzowanie i higiena konta. Każdy punkt to dodatkowe 1–3% efektywności. Zaplanować w cyklu kwartalnym.", style_body),
        ],
    ]
    leg = Table(leg_data, colWidths=[16 * mm, 30 * mm, 130 * mm])
    leg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), RED),
        ("BACKGROUND", (0, 1), (0, 1), AMBER),
        ("BACKGROUND", (0, 2), (0, 2), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (1, 0), (-1, -2), 0.5, SLATE_200),
        ("BOX", (0, 0), (-1, -1), 0.5, SLATE_200),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    story.append(leg)

    story.append(Spacer(1, 20))
    story.append(Paragraph("PROPONOWANY WORKFLOW", style_kicker))
    workflow_steps = [
        ("1.", "Przeczytaj <b>każde pytanie</b> i wpisz status w kolumnie po prawej: OK / DO POPRAWY / NIE WIEM."),
        ("2.", "Wszystkie „DO POPRAWY” z priorytetem P1 – to Twoja lista zadań na <b>najbliższe 7 dni</b>."),
        ("3.", "P2 – rozdziel na 2–4 tygodnie. P3 – zaplanuj w kwartalnym przeglądzie konta."),
        ("4.", "Wszystkie „NIE WIEM” – to obszary, w których potrzebujesz pomocy lub szkolenia zespołu."),
    ]
    for num, text in workflow_steps:
        wf = Table([[
            Paragraph("<b>%s</b>" % num, ParagraphStyle("wfnum", parent=styles["Normal"],
                                                       fontName=FONT_BOLD, fontSize=14, textColor=BLUE)),
            Paragraph(text, style_body),
        ]], colWidths=[10 * mm, 165 * mm])
        wf.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(wf)

    story.append(PageBreak())

    # === KATEGORIE ===
    for cat_idx, cat in enumerate(CATEGORIES):
        story.append(Paragraph(cat["range"].upper(), style_section_label))
        story.append(Paragraph(cat["name"], style_section_title))
        story.append(Paragraph(cat["intro"], style_section_intro))

        for item in cat["items"]:
            num_cell = Paragraph(
                "<font size='22' color='#1D4ED8'><b>%02d</b></font>" % item["n"],
                ParagraphStyle("numStyle", parent=styles["Normal"], alignment=TA_CENTER, leading=24)
            )

            prio_c = priority_color(item["priority"])
            prio_cell = Table(
                [[Paragraph("<b>%s</b>" % item["priority"], style_prio)]],
                colWidths=[12 * mm], rowHeights=[7 * mm]
            )
            prio_cell.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), prio_c),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ROUNDEDCORNERS", [3, 3, 3, 3]),
            ]))

            title_table = Table([[
                Paragraph(item["title"], style_item_title),
                prio_cell,
            ]], colWidths=[119 * mm, 14 * mm])
            title_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))

            micro_style = ParagraphStyle("micro", parent=styles["Normal"], fontName=FONT_BOLD,
                                         fontSize=7.5, textColor=SLATE_400, leading=10, spaceAfter=2)

            body_parts = [
                title_table,
                Spacer(1, 2),
                Paragraph("<font color='#94A3B8'><b>DLACZEGO MA ZNACZENIE</b></font>", micro_style),
                Paragraph(item["why"], style_item_body),
                Spacer(1, 4),
                Paragraph("<font color='#94A3B8'><b>CO SPRAWDZIĆ</b></font>", micro_style),
                Paragraph(item["check"], style_item_body),
            ]

            status_box = Table(
                [
                    [Paragraph("<b>STATUS</b>", ParagraphStyle("statusLabel", parent=styles["Normal"],
                                                               fontName=FONT_BOLD, fontSize=7.5,
                                                               textColor=SLATE_400, alignment=TA_CENTER))],
                    [Paragraph(" ", style_body)],
                    [Paragraph("<font color='#059669' face='%s'>[ ]</font>  OK" % FONT_BOLD, ParagraphStyle(
                        "s1", parent=styles["Normal"], fontName=FONT_NAME, fontSize=9,
                        textColor=SLATE_700, leading=14))],
                    [Paragraph("<font color='#D97706' face='%s'>[ ]</font>  Do poprawy" % FONT_BOLD, ParagraphStyle(
                        "s2", parent=styles["Normal"], fontName=FONT_NAME, fontSize=9,
                        textColor=SLATE_700, leading=14))],
                    [Paragraph("<font color='#94A3B8' face='%s'>[ ]</font>  Nie wiem" % FONT_BOLD, ParagraphStyle(
                        "s3", parent=styles["Normal"], fontName=FONT_NAME, fontSize=9,
                        textColor=SLATE_700, leading=14))],
                ],
                colWidths=[28 * mm],
            )
            status_box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), SLATE_50),
                ("BOX", (0, 0), (-1, -1), 0.5, SLATE_200),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 1), (-1, -1), 1),
            ]))

            row = Table(
                [[num_cell, body_parts, status_box]],
                colWidths=[14 * mm, 135 * mm, 30 * mm],
            )
            row.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("BOX", (0, 0), (-1, -1), 0.5, SLATE_200),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LINEBEFORE", (1, 0), (1, 0), 1.5, BLUE),
            ]))

            story.append(KeepTogether(row))
            story.append(Spacer(1, 6))

        if cat_idx < len(CATEGORIES) - 1:
            story.append(PageBreak())

    # === STRONA KONCOWA ===
    story.append(PageBreak())
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("CO DALEJ", style_kicker))
    story.append(Paragraph("Znalazłeś luki. Co teraz?", style_centered_h2))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Jeśli większość punktów z priorytetem P1 jest „do poprawy” lub „nie wiem” – "
        "Twoja konfiguracja przepala średnio 20–40% budżetu reklamowego miesięcznie. "
        "Im większe konto, tym większe straty w wartościach absolutnych.",
        style_centered_body
    ))
    story.append(Spacer(1, 20))

    cta_data = [[Paragraph(
        "<para alignment='center'>"
        "<font size='10' color='#93C5FD'><b>OFERTA DLA E-COMMERCE</b></font><br/><br/>"
        "<font size='18' color='#FFFFFF'><b>Pełny audyt Paid Media</b></font><br/><br/>"
        "<font size='10' color='#DBEAFE'>Diagnoza wszystkich 30 punktów + plan naprawy<br/>"
        "i wdrożenie krytycznych zmian w 2 tygodnie.</font><br/><br/>"
        "<font size='9' color='#93C5FD'>Realizacja na realnych danych – nie z teorii.<br/>"
        "8+ lat doświadczenia, 20+ rynków, portfolio: Vasco Electronics, Biedronka, Domodi."
        "</font></para>",
        ParagraphStyle("cta", parent=styles["Normal"], fontName=FONT_NAME, fontSize=10,
                       textColor=colors.white, leading=14)
    )]]
    cta = Table(cta_data, colWidths=[170 * mm])
    cta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 28),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ]))
    story.append(cta)
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "<para alignment='center'><font color='#475569'>Zamów audyt na stronie </font>"
        "<font color='#1D4ED8'><b>dawidrubin.pl/#audit</b></font></para>",
        ParagraphStyle("link", parent=styles["Normal"], fontName=FONT_NAME, fontSize=11, leading=14)
    ))

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<para alignment='center'><font size='8' color='#94A3B8'>"
        "© 2026 Dawid Rubin. Checklista przeznaczona do użytku własnego i pracy z zespołem. "
        "Dystrybucja komercyjna – tylko za zgodą autora."
        "</font></para>",
        ParagraphStyle("copy", parent=styles["Normal"], fontName=FONT_NAME, fontSize=8, leading=11)
    ))

    doc.build(story)
    print(f"PDF wygenerowany: {output_path}")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "audyt-paid-media-checklista.pdf")
    make_pdf(output)
