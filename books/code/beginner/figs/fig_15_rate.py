import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "15"

# 逐维相乘得到的三笔账：像素个数、潜变量个数、切 patch 后的 token 数
configs = [
    ("512²×49", 3 * 512 * 512 * 49, 16 * 64 * 64 * 13, 32 * 32 * 13),
    ("720×480×49", 3 * 720 * 480 * 49, 16 * 90 * 60 * 13, 45 * 30 * 13),
    ("1280×720×121", 3 * 1280 * 720 * 121, 16 * 160 * 90 * 31, 80 * 45 * 31),
    ("1920×1080×241", 3 * 1920 * 1080 * 241, 16 * 240 * 135 * 61, 120 * 67 * 61),
]

fig, ax = plt.subplots(figsize=(W_FULL * 1.02, 2.55))
x = np.arange(len(configs))
w = 0.26
series = [
    ("像素个数", [c[1] for c in configs], BLUE_L),
    ("潜变量个数", [c[2] for c in configs], BLUE),
    ("patch token 数", [c[3] for c in configs], GREEN),
]
for k, (label, vals, color) in enumerate(series):
    ax.bar(x + (k - 1) * w, vals, width=w * 0.92, color=color, label=label)

ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels([c[0] for c in configs], fontsize=8.0)
ax.set_ylabel("个数（对数）")
ax.set_ylim(5e3, 5e9)
ax.legend(loc="upper left", ncol=1, handlelength=1.2, borderaxespad=0.2)
ax.text(2.55, 2.2e8, "分辨率与长度一起涨，\ntoken 数涨得最快", fontsize=7.2, color=GRAY,
        ha="center", va="center", linespacing=1.6)
style(ax, grid=True, spines=("top", "right"))
save(fig, "fig15_rate", CH)
