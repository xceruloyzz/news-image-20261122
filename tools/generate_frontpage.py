#!/usr/bin/env python3
"""Deterministic newspaper front-page renderer for 22 November 2026.

Renders entry.png (1024x1024) with Pillow. No network access: every story
below is hardcoded from the day's reporting. The output is deterministic —
running this script twice produces byte-identical files.

Layout (all heights are measured from the wrapped text, so nothing
overflows its box):
  - masthead with the paper name and the dateline
  - lead story: COP31 deadlock in Antalya
  - six secondary stories in a two-column grid
  - a black ticker strip along the bottom with six more headlines
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 36

PAPER = (247, 242, 231)
INK = (18, 18, 18)
ACCENT = (164, 22, 22)
NAVY = (16, 42, 84)
GOLD = (255, 196, 0)
CARD_BG = (255, 253, 247)
TICKER_BG = (12, 12, 12)
TICKER_FG = (255, 255, 255)

SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]
SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns the list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def line_height(font, gap):
    ascent, descent = font.getmetrics()
    return ascent + descent + gap


def draw_lines(draw, x, y, lines, font, fill, gap):
    """Draw pre-wrapped lines; returns the y just below the last line."""
    step = line_height(font, gap)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


LEAD_KICKER = "LEAD STORY \u2022 ANTALYA, T\u00dcRKIYE"
LEAD_HEADLINE = "COP31 DEADLOCKED IN ANTALYA OVER FOSSIL FUELS"
LEAD_BODY = (
    "Climate talks ran a second day of overtime with no deal: the revised "
    "draft again omitted any explicit mention of coal, oil and gas, and "
    "the $120bn adaptation target was removed. EU envoy Wopke Hoekstra: "
    "\u201cBetter to have no deal than a bad deal.\u201d"
)

STORIES = [
    (
        "IRAN STRIKES BAHRAIN; TWO TANKERS HIT IN HORMUZ",
        "Bahrain: Iran hit a civilian industrial site \u2014 fire, no "
        "injuries. IRGC: it targeted US radar and bases. UKMTO: two "
        "tankers struck leaving the Strait of Hormuz.",
    ),
    (
        "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'",
        "Fausto Isidro Meza Flores, on the FBI ten most wanted list, was "
        "arrested in Sinaloa. Seven alleged gunmen and four soldiers "
        "died \u2014 11 killed.",
    ),
    (
        "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "Trilateral meeting in Shenzhen: the leaders agreed to begin "
        "talks on nuclear risk reduction.",
    ),
    (
        "RUSSIA HITS ZELENSKY'S HOMETOWN KRYVYI RIH",
        "Ballistic missile strike on Kryvyi Rih: two killed, dozens "
        "wounded. Ukraine said it hit a Russian ship.",
    ),
    (
        "US STOCKS FALL INTO CORRECTION IN AI SELL-OFF",
        "Dow and S&P 500 into correction in the AI sell-off: S&P 500 "
        "\u22123.7%, Nikkei \u22125.06%.",
    ),
    (
        "EU AND INDONESIA SIGN TRADE DEAL AFTER TEN YEARS",
        "The deal removes 98.5% of tariffs on EU goods and covers 730 "
        "million people, after ten years of talks.",
    ),
]

TICKER_LABEL = "ALSO ON 22 NOVEMBER:"
TICKER_ITEMS = [
    "Nigeria boat carrying funeral mourners capsizes, 24 dead",
    "Denmark expels Russian attach\u00e9 over alleged plot",
    "Fake liquor kills at least 11 in India's Manipur",
    "ICJ rules Myanmar committed genocide against Rohingya",
    "Kansas City Current win NWSL Championship",
    "Alcaraz to play Zverev in ATP Finals final",
]


def render(output_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    inner_w = WIDTH - 2 * MARGIN

    # --- Ticker geometry first: it anchors the bottom of the page. -----
    ticker_label_font = load_font(SANS_BOLD, 25)
    ticker_font = load_font(SANS, 21)
    ticker_text = "  \u2022  ".join(TICKER_ITEMS)
    ticker_lines = wrap(draw, ticker_text, ticker_font, inner_w)
    ticker_h = 12 + line_height(ticker_label_font, 2) + 4
    ticker_h += len(ticker_lines) * line_height(ticker_font, 3) + 12
    ticker_y = HEIGHT - ticker_h

    # --- Masthead --------------------------------------------------------
    masthead_font = load_font(SERIF_BOLD, 66)
    dateline_font = load_font(SANS_BOLD, 25)
    title = "THE WORLD TODAY"
    title_w = draw.textlength(title, font=masthead_font)
    draw.text(((WIDTH - title_w) / 2, 14), title, font=masthead_font, fill=INK)
    draw.line([(MARGIN, 102), (WIDTH - MARGIN, 102)], fill=INK, width=5)
    dateline = "SUNDAY, 22 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE IMAGE"
    dl_w = draw.textlength(dateline, font=dateline_font)
    draw.text(((WIDTH - dl_w) / 2, 112), dateline, font=dateline_font, fill=NAVY)
    draw.line([(MARGIN, 150), (WIDTH - MARGIN, 150)], fill=INK, width=2)

    # --- Lead story ------------------------------------------------------
    kicker_font = load_font(SANS_BOLD, 24)
    lead_head_font = load_font(SERIF_BOLD, 44)
    lead_body_font = load_font(SERIF, 21)
    lead_x = MARGIN + 20
    lead_w = inner_w - 40
    lead_head_lines = wrap(draw, LEAD_HEADLINE, lead_head_font, lead_w)
    lead_body_lines = wrap(draw, LEAD_BODY, lead_body_font, lead_w)
    lead_h = 12 + line_height(kicker_font, 2) + 4
    lead_h += len(lead_head_lines) * line_height(lead_head_font, 1) + 6
    lead_h += len(lead_body_lines) * line_height(lead_body_font, 3) + 12
    lead_y = 162
    draw.rectangle([MARGIN, lead_y, WIDTH - MARGIN, lead_y + lead_h],
                   fill=CARD_BG, outline=ACCENT, width=4)
    y = lead_y + 12
    draw.text((lead_x, y), LEAD_KICKER, font=kicker_font, fill=ACCENT)
    y += line_height(kicker_font, 2) + 4
    y = draw_lines(draw, lead_x, y, lead_head_lines, lead_head_font, INK, 1)
    y += 6
    draw_lines(draw, lead_x, y, lead_body_lines, lead_body_font, INK, 3)

    # --- Secondary stories: two columns, three rows ----------------------
    stories_y = lead_y + lead_h + 14
    gap = 12
    col_w = (inner_w - gap) // 2
    text_w = col_w - 24
    available = ticker_y - 12 - stories_y
    # Shrink the story fonts (deterministically) until the grid fits.
    for head_size, body_size in ((23, 19), (22, 18), (21, 17), (20, 16)):
        head_font = load_font(SANS_BOLD, head_size)
        body_font = load_font(SANS, body_size)
        wrapped = []
        row_heights = []
        for row in range(3):
            row_h = 0
            for col in range(2):
                headline, body = STORIES[row * 2 + col]
                hl = wrap(draw, headline, head_font, text_w)
                bl = wrap(draw, body, body_font, text_w)
                wrapped.append((hl, bl))
                card_h = 10 + len(hl) * line_height(head_font, 1) + 3
                card_h += len(bl) * line_height(body_font, 2) + 10
                row_h = max(row_h, card_h)
            row_heights.append(row_h)
        if sum(row_heights) + 2 * gap <= available:
            break
    y = stories_y
    for row in range(3):
        for col in range(2):
            hl, bl = wrapped[row * 2 + col]
            x0 = MARGIN + col * (col_w + gap)
            draw.rectangle([x0, y, x0 + col_w, y + row_heights[row]],
                           fill=CARD_BG, outline=INK, width=2)
            cy = draw_lines(draw, x0 + 12, y + 10, hl, head_font, NAVY, 1)
            draw_lines(draw, x0 + 12, cy + 3, bl, body_font, INK, 2)
        y += row_heights[row] + gap

    # --- Ticker strip ------------------------------------------------------
    draw.rectangle([0, ticker_y, WIDTH, HEIGHT], fill=TICKER_BG)
    draw.text((MARGIN, ticker_y + 12), TICKER_LABEL,
              font=ticker_label_font, fill=GOLD)
    ty = ticker_y + 12 + line_height(ticker_label_font, 2) + 4
    draw_lines(draw, MARGIN, ty, ticker_lines, ticker_font, TICKER_FG, 3)

    img.save(output_path, format="PNG", optimize=True)
    return output_path


def main():
    out = Path(__file__).resolve().parent.parent / "entry.png"
    render(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
