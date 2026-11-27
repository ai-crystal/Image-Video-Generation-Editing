#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""系列书的构建脚本：Markdown -> HTML -> PDF（Chrome 无头打印）。

用法：
    python books/build/build.py --book books/beginner
    python books/build/build.py --book books/beginner --figures    # 先重画插图
    python books/build/build.py --all                              # 构建全部册
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse

import markdown
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "books", "build")
COMMON = os.path.join(ROOT, "books", "common")
MAX_MB = 20.0
COMMON_URI = "file:///" + COMMON.replace("\\", "/")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise RuntimeError("找不到 Chrome 或 Edge，无法打印 PDF")


# ---------------------------------------------------------------- markdown

MATH_TOKEN = "@@MATH%d@@"
MATH_RE = re.compile(r"\$\$.+?\$\$|\$[^$\n]+?\$", re.S)


def protect_math(text):
    store = []

    def repl(m):
        store.append(m.group(0))
        return MATH_TOKEN % (len(store) - 1)

    return MATH_RE.sub(repl, text), store


def restore_math(html, store):
    for i, s in enumerate(store):
        # 公式里的 < > & 必须转义，否则 HTML 解析会把它们当成标签
        safe = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace(MATH_TOKEN % i, safe)
    return html


def md_to_html_simple(text, base_image_prefix):
    text, store = protect_math(text)
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists", "attr_list", "md_in_html"],
        output_format="html5",
    )
    html = restore_math(html, store)

    def repl(m):
        attrs = m.group(1)
        alt_m = re.search(r'alt="([^"]*)"', attrs)
        alt = alt_m.group(1) if alt_m else ""
        src_m = re.search(r'src="([^"]+)"', attrs)
        if not src_m:
            return m.group(0)
        src = src_m.group(1)
        if not src.startswith(("http", "file:", "data:")):
            src = urllib.parse.urljoin(base_image_prefix, src)
        return ('<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>'
                % (src, alt, alt))

    return re.sub(r"<p>\s*<img([^>]*)>\s*</p>", repl, html)


# ---------------------------------------------------------------- html

CSS = r"""
@page { size: 176mm 250mm; margin: 20mm 18mm 18mm 18mm; }
@page cover { margin: 0; }
@page back { margin: 0; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;
       font-size: 10.5pt; line-height: 1.74; color: #1b1b1b; text-align: justify; }

.cover, .backcover { page: cover; width: 176mm; height: 250mm; position: relative;
       overflow: hidden; page-break-after: always; }
.backcover { page: back; }
.cover .bg, .backcover .bg { position: absolute; inset: 0; width: 100%; height: 100%;
       object-fit: cover; }
.cover .shade { position: absolute; inset: 0;
       background: linear-gradient(160deg, rgba(8,12,24,.72) 0%, rgba(8,12,24,.45) 45%, rgba(8,12,24,.82) 100%); }
.cover .inner { position: absolute; left: 22mm; right: 22mm; top: 56mm; color: #fff; }
.cover .series { font-size: 11pt; letter-spacing: .28em; opacity: .9; }
.cover .rule { width: 38mm; height: 1.6pt; background: #e8c27a; margin: 7mm 0; }
.cover .title { font-size: 33pt; font-weight: 700; line-height: 1.15; letter-spacing: .04em; }
.cover .sub { font-size: 13pt; margin-top: 3mm; opacity: .95; }
.cover .vol { font-size: 14pt; margin-top: 12mm; opacity: .85; letter-spacing: .1em; }
.cover .author { position: absolute; left: 22mm; bottom: 26mm; color: #fff; font-size: 12pt; }
.cover .year { position: absolute; right: 22mm; bottom: 26mm; color: #fff; font-size: 10pt; opacity: .8; }

.backcover .inner { position: absolute; left: 22mm; right: 22mm; bottom: 30mm; color: #fff; }
.backcover .line { font-size: 10pt; opacity: .9; line-height: 2; }

.frontpage { page-break-after: always; text-align: center; }
.titlepage { padding-top: 55mm; }
.titlepage .t { font-size: 26pt; font-weight: 700; line-height: 1.4; }
.titlepage .s { font-size: 13pt; color: #444; margin-top: 8mm; }
.titlepage .a { font-size: 12pt; margin-top: 40mm; }
.titlepage .p { font-size: 10pt; color: #666; margin-top: 6mm; }

.copyright { padding-top: 150mm; font-size: 9pt; color: #444; line-height: 2; text-align: left; }

.toc { page-break-after: always; }
.toc h1 { font-size: 20pt; text-align: center; margin: 8mm 0 10mm; font-weight: 700; }
.toc ul { list-style: none; margin: 0; padding: 0; }
.toc li { display: flex; align-items: baseline; margin: 2.1mm 0; font-size: 10.5pt; }
.toc li.l1 { font-weight: 700; margin-top: 4mm; }
.toc li.l2 { padding-left: 8mm; font-size: 9.8pt; color: #333; }
.toc .t { white-space: nowrap; }
.toc .dots { flex: 1; border-bottom: 0.6pt dotted #999; margin: 0 1.6mm 1mm; }
.toc .pg { font-variant-numeric: tabular-nums; }

.chapter { page-break-before: always; }
.chapter h1 { font-size: 21pt; font-weight: 700; margin: 6mm 0 2mm; line-height: 1.3; }
.chapter .chnum { font-size: 9pt; letter-spacing: .3em; color: #2f5d8a; font-weight: 700; }
.chapter .hr { height: 1.2pt; background: #2f5d8a; margin: 4mm 0 8mm; }
h2 { font-size: 13.6pt; font-weight: 700; margin: 8mm 0 3mm; page-break-after: avoid; }
h3 { font-size: 11.4pt; font-weight: 700; margin: 6mm 0 2.5mm; page-break-after: avoid; }
p { margin: 0 0 2.0mm; text-indent: 2em; }
p.noindent, figure + p { text-indent: 2em; }
strong { font-weight: 700; }
em { font-style: normal; font-weight: 700; color: #1b1b1b; }

figure { margin: 3mm 0 4mm; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; max-height: 70mm; }
figcaption { font-size: 8.8pt; color: #555; margin-top: 2.2mm; line-height: 1.6; text-align: center; }

table { border-collapse: collapse; width: 100%; margin: 4mm 0 5mm; font-size: 9.2pt; }
th, td { border: none; border-top: .6pt solid #333; border-bottom: .6pt solid #333;
         padding: 1.6mm 2mm; text-align: left; }
thead { display: table-header-group; }
thead th { border-top: 1.1pt solid #111; border-bottom: .6pt solid #333; }
tr { page-break-inside: avoid; }
tbody tr:last-child td { border-bottom: 1.1pt solid #111; }

pre { background: #f6f6f4; border: .5pt solid #ddd; border-radius: 1.5mm; padding: 3mm 4mm;
      font-family: "Consolas", monospace; font-size: 8.6pt; line-height: 1.6;
      page-break-inside: avoid; white-space: pre-wrap; }
code { font-family: "Consolas", monospace; font-size: 9pt; background: #f2f2ef; padding: 0 .6mm; }
pre code { background: none; padding: 0; }

blockquote { margin: 4mm 0; padding: 1mm 0 1mm 5mm; border-left: 2pt solid #cfd8e3; color: #333; }
blockquote p { text-indent: 0; }

ul, ol { margin: 2mm 0 3mm; padding-left: 7mm; }
li { margin: 1mm 0; }

.katex { font-size: 1.02em; }
.katex-display { margin: 4mm 0; }
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_cover(book, img_uri, back=False):
    title = book["title"]
    subtitle = book.get("subtitle", "")
    author = book.get("author", "")
    series = book.get("series", "")
    volume = book.get("volume_label", "")
    year = book.get("year", "")
    if not back:
        return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page {{ size: 176mm 250mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.cover {{ position: relative; width: 176mm; height: 250mm; overflow: hidden;
          font-family: "Noto Serif SC", serif; }}
.cover .bg {{ position: absolute; left: 0; top: 0; width: 176mm; height: 250mm;
              object-fit: cover; }}
.cover .shade {{ position: absolute; inset: 0;
      background: linear-gradient(160deg, rgba(8,12,24,.55) 0%, rgba(8,12,24,.28) 45%, rgba(8,12,24,.72) 100%); }}
.cover .inner {{ position: absolute; left: 22mm; right: 22mm; top: 56mm; color: #fff; }}
.cover .series {{ font-size: 10.5pt; letter-spacing: .28em; opacity: .92; }}
.cover .title {{ font-size: 33pt; font-weight: 700; line-height: 1.3; margin-top: 5mm; }}
.cover .rule {{ width: 38mm; height: 1.6pt; background: #e8c27a; margin: 9mm 0; }}
.cover .vol {{ font-size: 15pt; }}
.cover .sub {{ font-size: 13pt; margin-top: 3mm; opacity: .95; }}
.cover .author {{ position: absolute; left: 22mm; bottom: 24mm; color: #fff; font-size: 12pt; }}
.cover .year {{ position: absolute; right: 22mm; bottom: 24mm; color: #fff; font-size: 10pt; opacity: .85; }}
</style></head><body>
<div class="cover">
  <img class="bg" src="{img_uri}">
  <div class="shade"></div>
  <div class="inner">
    <div class="series">{esc(series)}</div>
    <div class="title">{esc(title)}</div>
    <div class="rule"></div>
    <div class="vol">{esc(volume)}</div>
    <div class="sub">{esc(subtitle)}</div>
  </div>
  <div class="author">{esc(author)}</div>
  <div class="year">{esc(year)}</div>
</div></body></html>"""

    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page {{ size: 176mm 250mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.back {{ position: relative; width: 176mm; height: 250mm; overflow: hidden;
         font-family: "Noto Serif SC", serif; }}
.back .bg {{ position: absolute; left: 0; top: 0; width: 176mm; height: 250mm; object-fit: cover; }}
.back .shade {{ position: absolute; inset: 0; background: rgba(8,12,24,.55); }}
.back .inner {{ position: absolute; left: 24mm; right: 24mm; bottom: 32mm; color: #fff; }}
.back .l1 {{ font-size: 12pt; letter-spacing: .1em; }}
.back .l2 {{ font-size: 10pt; margin-top: 4mm; opacity: .85; line-height: 1.9; }}
</style></head><body>
<div class="back">
  <img class="bg" src="{img_uri}">
  <div class="shade"></div>
  <div class="inner">
    <div class="l1">{esc(series)}　{esc(title)}</div>
    <div class="l2">{esc(volume)}　{esc(subtitle)}<br>{esc(author)}　{esc(year)}</div>
  </div>
</div></body></html>"""


def build_html(book, items, toc_entries, cover_uri, back_uri):
    title = book["title"]
    subtitle = book.get("subtitle", "")
    author = book.get("author", "")
    series = book.get("series", "")
    volume = book.get("volume_label", "")
    year = book.get("year", "")

    parts = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">',
             "<title>%s</title>" % esc(title),
             '<link rel="stylesheet" href="%s">' % (COMMON_URI + "/assets/katex/katex.min.css"),
             "<style>%s</style></head><body>" % CSS]

    # 扉页
    parts.append(f'''
<section class="frontpage titlepage">
  <div class="t">{esc(title)}</div>
  <div class="s">{esc(volume)}　{esc(subtitle)}</div>
  <div class="a">{esc(author)}</div>
  <div class="p">{esc(series)}　{esc(year)}</div>
</section>''')

    # 版权页
    parts.append(f'''
<section class="frontpage">
  <div class="copyright">
    <p style="text-indent:0">{esc(title)}</p>
    <p style="text-indent:0">{esc(subtitle)}</p>
    <p style="text-indent:0">作者：{esc(author)}</p>
    <p style="text-indent:0">版本：{esc(year)} 年第一版</p>
    <p style="text-indent:0">本书用于学习与研究，书中的推导与结论请以原始论文为准。</p>
  </div>
</section>''')

    # 目录
    parts.append('<section class="toc"><h1>目　录</h1><ul>')
    for e in toc_entries:
        cls = "l%d" % e["level"]
        pg = e.get("page", "")
        parts.append('<li class="%s"><span class="t">%s</span><span class="dots"></span>'
                     '<span class="pg">%s</span></li>' % (cls, esc(e["title"]), pg))
    parts.append("</ul></section>")

    # 正文
    for it in items:
        if it["kind"] == "chapter":
            parts.append('<section class="chapter"><div class="chnum">第 %s 章</div>'
                         '<h1>%s</h1><div class="hr"></div>' % (it["num"], esc(it["title"])))
            parts.append(it["html"])
            parts.append("</section>")
        elif it["kind"] == "appendix":
            parts.append('<section class="chapter"><div class="chnum">附录 %s</div>'
                         '<h1>%s</h1><div class="hr"></div>' % (it["num"], esc(it["title"])))
            parts.append(it["html"])
            parts.append("</section>")
        else:
            parts.append('<section class="chapter">%s</section>' % it["html"])

    # KaTeX 渲染
    parts.append('<script src="%s/assets/katex/katex.min.js"></script>' % COMMON_URI)
    parts.append('<script src="%s/assets/katex/auto-render.min.js"></script>' % COMMON_URI)
    parts.append("""<script>
document.addEventListener("DOMContentLoaded", function () {
  renderMathInElement(document.body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "$", right: "$", display: false}
    ],
    throwOnError: false
  });
});
</script>""")
    parts.append("</body></html>")
    return "\n".join(parts)


# ---------------------------------------------------------------- pdf

def chrome_print(html_path, pdf_path):
    chrome = find_chrome()
    tmp = tempfile.mkdtemp(prefix="chrome-")
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--virtual-time-budget=30000",
           "--user-data-dir=" + tmp,
           "--print-to-pdf=" + pdf_path,
           "file:///" + html_path.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    shutil.rmtree(tmp, ignore_errors=True)
    if not os.path.exists(pdf_path):
        raise RuntimeError("Chrome 打印失败：\n%s\n%s" % (r.stdout[-2000:], r.stderr[-2000:]))


def compose(out_pdf, cover_html, body_html, back_html, work):
    """分别打印封面、正文、封底，再拼成一个 PDF。"""
    c = os.path.join(work, "_cover.pdf")
    b = os.path.join(work, "_body.pdf")
    k = os.path.join(work, "_back.pdf")
    chrome_print(cover_html, c)
    chrome_print(body_html, b)
    chrome_print(back_html, k)
    doc = pymupdf.open()
    for p in (c, b, k):
        src = pymupdf.open(p)
        doc.insert_pdf(src)
        src.close()
    doc.save(out_pdf)
    doc.close()


def extract_headings(pdf_path, sizes=(20.0, 13.0)):
    """返回 [(level, text, page_index)]，按出现顺序。"""
    doc = pymupdf.open(pdf_path)
    out = []
    for pno, page in enumerate(doc):
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                spans = [s for s in line.get("spans", []) if s["text"].strip()]
                if not spans:
                    continue
                size = max(s["size"] for s in spans)
                text = "".join(s["text"] for s in spans).strip()
                if size >= 18:
                    out.append((1, text, pno))
                elif size >= 11.8 and len(text) > 1:
                    out.append((2, text, pno))
    doc.close()
    # 合并同一页上重复
    dedup = []
    for lv, t, p in out:
        if dedup and dedup[-1][1] == t and dedup[-1][2] == p:
            continue
        dedup.append((lv, t, p))
    return dedup


def roman(n):
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, sym in vals:
        while n >= v:
            out += sym
            n -= v
    return out


def stamp_pdf(pdf_path, items, headings, book):
    doc = pymupdf.open(pdf_path)
    # 找第一章起始页
    first_title = next((it["title"] for it in items if it["kind"] in ("chapter", "appendix")), None)
    offset = 0
    for lv, t, p in headings:
        if first_title and first_title in t:
            offset = p
            break

    # 页码
    for i, page in enumerate(doc):
        if i == 0 or i == doc.page_count - 1:
            continue
        num = roman(i + 1) if i < offset else str(i - offset + 1)
        w = page.rect.width
        page.insert_text((w / 2 - 6, page.rect.height - 22), num,
                         fontsize=9, fontname="helv", color=(0.35, 0.35, 0.35))

    # 书签
    toc = [[1, book["title"], 1]]
    for lv, t, p in headings:
        if p < 2 or p >= doc.page_count - 1:
            continue
        t = t.strip()
        if not t or t in ("目　录", "目录"):
            continue
        toc.append([lv, t, p + 1])
    doc.set_toc(toc)
    doc.set_metadata({"title": book["title"], "author": book.get("author", ""),
                      "subject": book.get("subtitle", ""), "creator": "md + chrome"})
    doc.saveIncr()
    doc.close()
    return offset


def optimize(pdf_path, images, max_mb):
    if os.path.getsize(pdf_path) / 1024 / 1024 <= max_mb:
        return True
    print("  PDF 超过 %.0f MB，压缩插图后重建" % max_mb)
    try:
        from PIL import Image
    except ImportError:
        return False
    for p in images:
        if p.lower().endswith(".png"):
            im = Image.open(p).convert("RGB")
            im.save(p, "PNG", optimize=True)
    return False


# ---------------------------------------------------------------- main


def load(bookdir):
    book = json.load(open(os.path.join(bookdir, "book.json"), encoding="utf-8"))
    struct = json.load(open(os.path.join(bookdir, "structure.json"), encoding="utf-8"))
    return book, struct


def collect(bookdir, struct):
    items = []
    for sec in struct["sections"]:
        kind = sec.get("kind", "chapter")
        for i, ch in enumerate(sec["items"]):
            path = os.path.join(bookdir, ch["file"])
            if not os.path.exists(path):
                raise RuntimeError("缺少文件：%s" % path)
            text = open(path, encoding="utf-8").read()
            html = md_to_html_simple(text, "file:///" + os.path.dirname(path).replace("\\", "/") + "/")
            if kind != "front":
                html = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S)
            items.append({
                "kind": kind,
                "num": ch.get("num", i + 1),
                "title": ch["title"],
                "file": ch["file"],
                "html": html,
            })
    return items


CROSS_PATTERNS = [
    r"(入门|进阶|深入|基础|高级|实战|专题|提高)篇",
    r"下一[册本]",
    r"上一[册本]",
    r"第[一二三四五六七八九]册",
    r"这套书",
    r"本系列",
]


def check_cross_refs(bookdir, book):
    """检查正文里是否引用了其他分册。只警告，不中断构建。"""
    own = {book.get("volume_label", ""), book.get("title", ""), book.get("series", "")}
    own = {x for x in own if x}
    hits = []
    for f in sorted(glob.glob(os.path.join(bookdir, "**", "*.md"), recursive=True)):
        if os.path.basename(f).lower() in ("readme.md",):
            continue
        rel = os.path.relpath(f, bookdir)
        for lineno, line in enumerate(open(f, encoding="utf-8"), 1):
            for pat in CROSS_PATTERNS:
                for m in re.finditer(pat, line):
                    text = m.group(0)
                    if text in own:
                        continue
                    hits.append((rel, lineno, text, line.strip()[:60]))
    if hits:
        print("  提示：发现 %d 处可能的分册引用（建议改成不依赖其他分册的写法）" % len(hits))
        for rel, lineno, text, ctx in hits[:20]:
            print("    %s:%d  %s  | %s" % (rel, lineno, text, ctx))
    else:
        print("  分册引用检查：通过")
    return hits


def check_images(bookdir):
    """检查正文引用的图片是否都存在。"""
    miss = []
    for f in glob.glob(os.path.join(bookdir, "**", "*.md"), recursive=True):
        if os.path.basename(f).lower() == "readme.md":
            continue
        text = open(f, encoding="utf-8").read()
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
            rel = m.group(1)
            if rel.startswith("http"):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), rel))
            if not os.path.exists(target):
                miss.append((os.path.relpath(f, bookdir), rel))
    if miss:
        print("  警告：%d 个图片路径不存在" % len(miss))
        for f, rel in miss[:10]:
            print("    %s -> %s" % (f, rel))
    else:
        print("  图片路径检查：通过")
    return miss


def build_book(bookdir, do_figures=False, no_opt=False):
    bookdir = os.path.abspath(bookdir)
    book, struct = load(bookdir)
    print("=" * 56)
    print(" 构建：%s" % book["title"])
    print("=" * 56)

    if do_figures:
        run_figures(bookdir)

    check_cross_refs(bookdir, book)
    check_images(bookdir)
    items = collect(bookdir, struct)
    imgs = sorted(glob.glob(os.path.join(bookdir, "images", "**", "*.png"), recursive=True))
    cover = os.path.join(bookdir, "images", book.get("cover", "cover.jpg"))
    back = os.path.join(bookdir, "images", book.get("backcover", "backcover.jpg"))
    cover_uri = "file:///" + cover.replace("\\", "/")
    back_uri = "file:///" + back.replace("\\", "/")

    out_pdf = os.path.join(ROOT, "output", book["pdf"])
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)

    work = os.path.join(ROOT, "books", "build", ".work", book["name"])
    os.makedirs(work, exist_ok=True)

    # 第一遍：无页码目录
    toc_entries = []
    for it in items:
        toc_entries.append({"title": ("第 %s 章　%s" % (it["num"], it["title"])) if it["kind"] == "chapter"
                            else ("附录 %s　%s" % (it["num"], it["title"])) if it["kind"] == "appendix"
                            else it["title"], "level": 1})
        for h in re.findall(r"<h2[^>]*>(.*?)</h2>", it["html"], re.S):
            toc_entries.append({"title": re.sub(r"<[^>]+>", "", h), "level": 2})

    html = build_html(book, items, toc_entries, cover_uri, back_uri)
    html_path = os.path.join(work, "book.html")
    open(html_path, "w", encoding="utf-8").write(html)
    cover_path = os.path.join(work, "cover.html")
    open(cover_path, "w", encoding="utf-8").write(build_cover(book, cover_uri))
    back_path = os.path.join(work, "back.html")
    open(back_path, "w", encoding="utf-8").write(build_cover(book, back_uri, back=True))
    t0 = time.time()
    compose(out_pdf, cover_path, html_path, back_path, work)

    heads = extract_headings(out_pdf)
    offset = stamp_pdf(out_pdf, items, heads, book)

    # 补页码后重排目录：按文档顺序逐条对齐，标题重名时不会错位
    def clean(e):
        key = e["title"]
        if key.startswith("第 ") and "章　" in key:
            key = key.split("章　", 1)[1]
        elif key.startswith("附录 ") and "　" in key:
            key = key.split("　", 1)[1]
        return key.strip()

    hi = 0
    for e in toc_entries:
        e["page"] = ""
        want_lv = 2 if e["level"] == 2 else 1
        key = clean(e)
        for j in range(hi, len(heads)):
            lv, t, p = heads[j]
            if lv == want_lv and t.strip() == key:
                e["page"] = p - offset + 1 if p >= offset else roman(p + 1)
                hi = j + 1
                break
    miss = [clean(e) for e in toc_entries if e["page"] == ""]
    if miss:
        print("  目录页码未对上：%s" % miss[:5])

    html = build_html(book, items, toc_entries, cover_uri, back_uri)
    open(html_path, "w", encoding="utf-8").write(html)
    compose(out_pdf, cover_path, html_path, back_path, work)
    stamp_pdf(out_pdf, items, extract_headings(out_pdf), book)

    size = os.path.getsize(out_pdf) / 1024 / 1024
    if size > MAX_MB and not no_opt:
        if optimize(out_pdf, imgs, MAX_MB):
            compose(out_pdf, cover_path, html_path, back_path, work)
            stamp_pdf(out_pdf, items, extract_headings(out_pdf), book)
    doc = pymupdf.open(out_pdf)
    pages = doc.page_count
    doc.close()
    print("完成：%d 页，%.2f MB，用时 %.1f 秒" % (pages, os.path.getsize(out_pdf) / 1024 / 1024, time.time() - t0))
    print("输出：%s" % out_pdf)


def run_figures(bookdir):
    scripts = sorted(glob.glob(os.path.join(ROOT, "books", "code", "**", "fig_*.py"), recursive=True))
    if not scripts:
        return
    print("重画插图（%d 个脚本）" % len(scripts))
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    for s in scripts:
        r = subprocess.run([sys.executable, s], cwd=ROOT, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print("  [失败] %s\n%s" % (os.path.basename(s), (r.stderr or "")[-800:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--no-opt", action="store_true")
    args = ap.parse_args()

    if args.figures:
        run_figures(None)

    if args.all:
        dirs = [d for d in glob.glob(os.path.join(ROOT, "books", "*"))
                if os.path.exists(os.path.join(d, "book.json"))]
    elif args.book:
        dirs = [args.book]
    else:
        dirs = [os.path.join(ROOT, "books", "beginner")]

    for d in dirs:
        build_book(d, do_figures=False, no_opt=args.no_opt)


if __name__ == "__main__":
    main()
