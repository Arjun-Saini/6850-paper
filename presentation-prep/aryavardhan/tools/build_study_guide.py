"""Build study-guide.html from the prep Markdown files.

Run: python3 build_study_guide.py [--artifact OUT_FRAGMENT]
- Markdown -> HTML at build time (python-markdown); ```mermaid blocks -> inline SVG via mmdc (cached).
- figures/*.svg -> inline data URIs; tables wrapped for horizontal scroll; links between files -> tab links.
- 04-qa-bank.md -> flashcard JSON; explorer_math.js (exports stripped) + explorer.js inlined.
Writes ../study-guide.html (full document). --artifact also writes a body fragment for publishing.
"""
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(HERE)
CACHE = os.path.join(HERE, ".cache")
os.makedirs(CACHE, exist_ok=True)

LINKS = {
    "01-opening-summary.md": "opening", "02-our-work-explained.md": "our-work", "03-papers/": "papers",
    "03-papers/egl.md": "papers:egl", "03-papers/cnst.md": "papers:cnst", "03-papers/dgm.md": "papers:dgm",
    "03-papers/prior-work.md": "papers:prior", "03-papers/course-references.md": "papers:course",
    "04-qa-bank.md": "flashcards", "05-cheatsheet.md": "cheatsheet",
}
_diag = [0]


def mermaid_svg(src):
    _diag[0] += 1
    sid = f"diag-{_diag[0]}"
    key = hashlib.sha256((sid + src).encode()).hexdigest()[:16]
    cached = os.path.join(CACHE, key + ".svg")
    if not os.path.exists(cached):
        d = tempfile.mkdtemp()
        open(os.path.join(d, "in.mmd"), "w").write(src)
        out = os.path.join(d, "out.svg")
        r = subprocess.run(["mmdc", "-i", os.path.join(d, "in.mmd"), "-o", out, "-t", "neutral", "-b", "transparent",
                            "-I", sid, "-q"], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"mermaid failed ({sid}): {r.stderr[-300:]}")
        open(cached, "w").write(open(out).read())
    svg = open(cached).read()
    return re.sub(r"^<\?xml[^>]*>\s*", "", svg)


def figure(src_path, alt):
    data = base64.b64encode(open(src_path, "rb").read()).decode()
    cap = f"<figcaption>{html.escape(alt)}</figcaption>" if alt else ""
    return f'<figure class="figure"><img src="data:image/svg+xml;base64,{data}" alt="{html.escape(alt)}">{cap}</figure>'


def md_to_html(path):
    text = open(path).read()
    base = os.path.dirname(path)
    blocks = []

    def stash(m):
        blocks.append(mermaid_svg(m.group(1)))
        return f"\n\nMERMAIDBLOCK{len(blocks) - 1}\n\n"

    text = re.sub(r"```mermaid\n(.*?)```", stash, text, flags=re.S)
    out = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    out = re.sub(r"<p>MERMAIDBLOCK(\d+)</p>", lambda m: f'<div class="diagram">{blocks[int(m.group(1))]}</div>', out)

    def img(m):
        src, alt = m.group(2), html.unescape(m.group(1))
        return figure(os.path.normpath(os.path.join(base, src)), alt)

    out = re.sub(r'<p><img alt="([^"]*)" src="([^"]+\.svg)" ?/?></p>', img, out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    def link(m):
        href, label = m.group(1), m.group(2)
        rel = os.path.relpath(os.path.normpath(os.path.join(base, href)), PREP).replace(os.sep, "/")
        if href.endswith("/"):
            rel += "/"
        tgt = LINKS.get(rel)
        return f'<a href="#{tgt.split(":")[0]}" data-goto="{tgt}">{label}</a>' if tgt else m.group(0)

    out = re.sub(r'<a href="([^"#:]+?\.md|[^"#:]+/)">(.*?)</a>', link, out)
    return out


def inline_md(s):
    h = markdown.markdown(s.strip())
    return re.sub(r"^<p>|</p>$", "", h.strip())


def parse_cards(path):
    cards, group, title = [], None, None
    for part in re.split(r"^(?=## |### Q)", open(path).read(), flags=re.M):
        m = re.match(r"## ([A-I])\. (.+)", part)
        if m:
            group, title = m.group(1), m.group(2).strip()
            continue
        m = re.match(r"### Q(\w+)\. (.+?)\n(.*)", part, re.S)
        if not m:
            continue
        q, body = m.group(2).strip(), m.group(3)
        star = q.endswith("★")
        q = q.rstrip(" ★")
        short = re.search(r"\*\*Short:\*\*(.*?)(?=\*\*If pushed:\*\*)", body, re.S)
        pushed = re.search(r"\*\*If pushed:\*\*(.*?)(?=\n---|\Z|\n## )", body, re.S)
        cards.append({"id": m.group(1), "group": group, "groupTitle": f"{group}. {title}", "q": inline_md(q),
                      "star": star, "short": inline_md(short.group(1)), "pushed": inline_md(pushed.group(1))})
    return cards


def build():
    tpl = open(os.path.join(HERE, "study_guide_template.html")).read()
    parts = {
        "OPENING": md_to_html(os.path.join(PREP, "01-opening-summary.md")),
        "OURWORK": md_to_html(os.path.join(PREP, "02-our-work-explained.md")),
        "EGL": md_to_html(os.path.join(PREP, "03-papers", "egl.md")),
        "CNST": md_to_html(os.path.join(PREP, "03-papers", "cnst.md")),
        "DGM": md_to_html(os.path.join(PREP, "03-papers", "dgm.md")),
        "PRIOR": md_to_html(os.path.join(PREP, "03-papers", "prior-work.md")),
        "COURSE": md_to_html(os.path.join(PREP, "03-papers", "course-references.md")),
        "QABANK": md_to_html(os.path.join(PREP, "04-qa-bank.md")),
        "CHEATSHEET": md_to_html(os.path.join(PREP, "05-cheatsheet.md")),
        "CARDS_JSON": json.dumps(parse_cards(os.path.join(PREP, "04-qa-bank.md")), ensure_ascii=False).replace("</", "<\\/"),
        "EXPLORER_MATH": re.sub(r"^export ", "", open(os.path.join(HERE, "explorer_math.js")).read(), flags=re.M),
        "EXPLORER_UI": open(os.path.join(HERE, "explorer.js")).read(),
    }
    for k, v in parts.items():
        assert "{{" + k + "}}" in tpl, k
        tpl = tpl.replace("{{" + k + "}}", v)
    assert "{{" not in tpl, "unfilled placeholder"
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '</head>\n<body>\n' + tpl + '\n</body>\n</html>\n')
    open(os.path.join(PREP, "study-guide.html"), "w").write(full)
    print(f"wrote study-guide.html ({len(full) // 1024} KB, {_diag[0]} diagrams, {len(parts['CARDS_JSON'])} B cards)")
    if "--artifact" in sys.argv:
        out = sys.argv[sys.argv.index("--artifact") + 1]
        open(out, "w").write(tpl)
        print("wrote artifact fragment", out)


if __name__ == "__main__":
    build()
