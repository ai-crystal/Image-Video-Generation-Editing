import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.ticker import NullFormatter, LogLocator

CH = "11"

# ---------- 图 11.3 分辨率与两种开销 ----------
sides = np.array([256, 300, 384, 512, 640, 768, 1024], dtype=float)
pix_tok = sides ** 2
lat_tok = (sides / 8.0) ** 2
pix_attn = sides ** 4
lat_attn = (sides / 8.0) ** 4

fig, ax = plt.subplots(figsize=(W_FULL * 0.95, 2.5))
ax.loglog(sides, pix_attn, color=RED, lw=1.6, ls="-")
ax.loglog(sides, lat_attn, color=RED, lw=1.6, ls=(0, (4, 2)))
ax.loglog(sides, pix_tok, color=BLUE, lw=1.4, ls="-")
ax.loglog(sides, lat_tok, color=BLUE, lw=1.4, ls=(0, (4, 2)))

ax.axhline(1e9, color=GRAY, lw=0.8, ls=(0, (1, 3)))
ax.text(262, 1.15e9, "fp16 下约 2 GB", fontsize=7.2, color=GRAY, va="bottom")

ax.set_xlim(250, 1360)
ax.set_ylim(4e3, 2.2e12)
ax.set_xticks([256, 384, 512, 768, 1024])
ax.set_xticklabels(["256", "384", "512", "768", "1024"])
ax.xaxis.set_minor_formatter(NullFormatter())
ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=12))
ax.set_xlabel("图像边长 $S$（像素）")
ax.set_ylabel("数值个数")
style(ax, grid=True)

ax.annotate("", xy=(512, 1.68e7), xytext=(512, 6.87e10),
            arrowprops=dict(arrowstyle="<|-|>", color=PURPLE, lw=0.9, shrinkA=0, shrinkB=0))
ax.text(524, 8.0e8, "4096 倍", fontsize=7.6, color=PURPLE, va="center")

labels = [
    (pix_attn[-1], "$S^4$\n像素注意力", RED),
    (lat_attn[-1], "$(S/8)^4$\n潜空间注意力", RED),
    (pix_tok[-1], "$S^2$\n像素 token", BLUE),
    (lat_tok[-1], "$(S/8)^2$\n潜空间 token", BLUE),
]
for yv, txt, c in labels:
    ax.text(1050, yv, txt, fontsize=7.0, color=c, va="center", ha="left", linespacing=1.35)
save(fig, "fig11_compute", CH)

# ---------- 图 11.4 长宽比分桶 ----------
buckets = [(320, 768), (384, 640), (448, 576), (512, 512),
           (576, 448), (640, 384), (704, 320), (768, 320)]
AREA = 512 * 512
S = 0.0020
GAP = 0.45

fig, ax = plt.subplots(figsize=(W_FULL * 0.95, 2.1))
ax.set_xlim(0, 13.35)
ax.set_ylim(-0.95, 3.35)
ax.axis("off")

x = 0.5
pos = {}
for (w, h) in buckets:
    sw = AREA / h * S
    sh = h * S
    hit = (w, h) == (576, 448)
    ax.add_patch(plt.Rectangle((x, 0), sw, sh,
                               fc="#f6e9d2" if hit else "#eaf0f6",
                               ec=SAND if hit else BLUE, lw=1.0 if hit else 0.8))
    ax.text(x + sw / 2, -0.12, "%d×%d" % (w, h), ha="center", va="top", fontsize=6.5,
            color=INK if hit else GRAY, rotation=90)
    pos[(w, h)] = (x + sw / 2, sh)
    x += sw + GAP

ax.text(6.4, 2.95, "每个桶的面积都是 $512^2\\approx 26.2$ 万像素，只是形状不同", fontsize=7.5,
        color=GRAY, ha="center")
cx, ch = pos[(576, 448)]
ax.annotate("4:3 的图归到这个桶", xy=(cx, ch + 0.05), xytext=(cx - 0.55, 2.45), fontsize=7.3,
            color=SAND, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9))
save(fig, "fig11_bucket", CH)
