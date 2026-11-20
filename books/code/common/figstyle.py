import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_parts = os.path.abspath(sys.argv[0]).replace("\\", "/").split("/")
BOOK_NAME = _parts[_parts.index("code") + 1] if "code" in _parts else "beginner"
BOOK = os.path.join(ROOT, "books", BOOK_NAME)
FONTDIR = os.path.join(ROOT, "_private", "assets", "fonts")

for _f in ("NotoSerifSC-Regular.ttf", "NotoSerifSC-Bold.ttf"):
    _p = os.path.join(FONTDIR, _f)
    if os.path.exists(_p):
        fm.fontManager.addfont(_p)

INK = "#1b1b1b"
BLUE = "#2f5d8a"
BLUE_L = "#7fa3c4"
RED = "#b4574c"
GREEN = "#4e7a5f"
SAND = "#c9a227"
PURPLE = "#6b5b8a"
GRAY = "#6b6b6b"
LIGHT = "#d9d9d6"

plt.rcParams.update({
    "font.family": "Noto Serif SC",
    "font.size": 9.5,
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "axes.edgecolor": "#4a4a4a",
    "axes.linewidth": 0.7,
    "axes.labelcolor": INK,
    "axes.labelsize": 9.5,
    "xtick.color": "#4a4a4a",
    "ytick.color": "#4a4a4a",
    "xtick.labelsize": 8.6,
    "ytick.labelsize": 8.6,
    "legend.frameon": False,
    "legend.fontsize": 8.4,
    "lines.linewidth": 1.5,
    "figure.dpi": 150,
    "savefig.dpi": 240,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
})

W_FULL = 5.0
W_HALF = 2.45


def style(ax, grid=False, spines=("top", "right")):
    for s in spines:
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, color=LIGHT, lw=0.6, alpha=0.9)
        ax.set_axisbelow(True)
    return ax


def save(fig, name, chapter=None):
    ch = chapter
    if ch is None:
        ch = os.path.basename(os.path.abspath(sys.argv[0])).split("_")[1][:2]
    outdir = os.path.join(BOOK, "images", ch)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name + ".png")
    fig.savefig(path, format="png")
    plt.close(fig)
    print("saved", os.path.relpath(path, ROOT), "%.0f KB" % (os.path.getsize(path) / 1024))
