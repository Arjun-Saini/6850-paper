"""Render check for study-guide.html (Playwright + Chromium).

Run: python3 render_check.py [screenshot_dir]
Asserts, at 1280x900 and 390x844:
  - no console errors (font-host failures ignored: offline sandboxes cannot reach Google Fonts)
  - every tab opens and shows content
  - every diagram container holds an <svg> with no "Syntax error"
  - the flashcard deck has as many cards as "### Q" headings in 04-qa-bank.md
  - the explorer's "pairs" preset shows pairs phi* in [0.165, 0.177], below both extremes
  - no horizontal page scroll at phone width
"""
import os
import re
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(HERE)
PAGE = os.path.join(PREP, "study-guide.html")
SHOTS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_shots")
TABS = ["opening", "our-work", "papers", "flashcards", "explorer", "cheatsheet"]
N_Q = len(re.findall(r"^### Q", open(os.path.join(PREP, "04-qa-bank.md")).read(), flags=re.M))
IGNORE = ("fonts.googleapis.com", "fonts.gstatic.com", "net::ERR_")

fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)


os.makedirs(SHOTS, exist_ok=True)
if not os.path.exists(PAGE):
    print("FAIL page missing:", PAGE)
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for w, h in ((1280, 900), (390, 844)):
        page = browser.new_page(viewport={"width": w, "height": h})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto("file://" + PAGE)
        page.wait_for_timeout(600)
        for tab in TABS:
            page.click(f'[data-tab="{tab}"]')
            page.wait_for_timeout(250)
            panel = page.locator(f"#panel-{tab}")
            check(panel.is_visible(), f"{w}px: panel {tab} not visible")
            check(len(panel.inner_text().strip()) > 200, f"{w}px: panel {tab} looks empty")
            page.screenshot(path=os.path.join(SHOTS, f"{w}-{tab}.png"), full_page=False)
            if w == 390:
                sw = page.evaluate("document.documentElement.scrollWidth")
                cw = page.evaluate("document.documentElement.clientWidth")
                check(sw <= cw, f"390px: horizontal scroll on {tab} ({sw} > {cw})")
        # diagrams
        n_diag = page.locator(".diagram").count()
        n_svg = page.locator(".diagram svg").count()
        check(n_diag >= 12 and n_svg == n_diag, f"diagrams: {n_svg} svgs in {n_diag} containers")
        check("Syntax error" not in page.content(), "a diagram shows a Mermaid syntax error")
        # flashcards
        page.click('[data-tab="flashcards"]')
        total = page.evaluate("window.__cards ? window.__cards.length : -1")
        check(total == N_Q, f"flashcards: {total} cards vs {N_Q} questions")
        page.click("#card")
        check(page.locator("#card .back").is_visible(), "flashcard does not flip")
        # explorer
        page.click('[data-tab="explorer"]')
        page.click('[data-preset="pairs"]')
        page.wait_for_timeout(1500)
        vals = page.evaluate("window.__explorer && window.__explorer.phiStars ? window.__explorer.phiStars : null")
        if not vals:
            check(False, "explorer: no phi* readout after pairs preset")
        else:
            ps = {int(k): v for k, v in vals.items()}
            check(0.165 <= ps.get(2, -1) <= 0.177, f"explorer: pairs phi* = {ps.get(2)}")
            check(ps.get(2, 1) < ps.get(1, 0) and ps.get(2, 1) < ps.get(4, 0), f"explorer: pairs not worst: {ps}")
        page.screenshot(path=os.path.join(SHOTS, f"{w}-explorer-pairs.png"), full_page=True)
        real = [e for e in errors if not any(s in e for s in IGNORE)]
        check(not real, f"{w}px console errors: {real[:3]}")
        page.close()
    browser.close()

if fails:
    print(f"FAIL {len(fails)}")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print(f"OK tabs={len(TABS)} cards={N_Q} widths=1280,390")
