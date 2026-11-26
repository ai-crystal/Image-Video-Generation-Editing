import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "20"

fig, ax = plt.subplots(figsize=(W_FULL, 2.3))
ax.set_xlim(0, 10.6)
ax.set_ylim(0, 5.9)
ax.axis("off")


def box(x, y, w, h, lines, fc="#eef2f6", ec=BLUE, fs=7.4):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, lines, ha="center", va="center", fontsize=fs,
            color=INK, linespacing=1.45)


box(0.15, 2.35, 1.30, 1.15, "$z$\n512 维")
box(1.95, 2.35, 1.75, 1.15, "映射网络\n8 层 MLP", fc="#f7f4ec", ec=SAND)
box(4.05, 2.35, 1.05, 1.15, "$w$\n512 维", fc="#eef6f0", ec=GREEN)

ax.annotate("", xy=(1.92, 2.92), xytext=(1.48, 2.92),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9, mutation_scale=7))
ax.annotate("", xy=(4.02, 2.92), xytext=(3.73, 2.92),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9, mutation_scale=7))

# 逐层展开
ys = np.linspace(5.05, 0.95, 9)
for y in ys:
    ax.add_patch(plt.Rectangle((6.15, y - 0.19), 0.62, 0.38, fc="#eef2f6", ec=BLUE_L, lw=0.6))
    ax.plot([5.12, 6.12], [2.92, y], color=BLUE_L, lw=0.55, alpha=0.75)

ax.text(6.46, 5.36, "风格层", fontsize=7.0, color=GRAY, ha="center", va="bottom")
ax.text(6.92, 4.83, "第 4–8 层：姿态、形状", fontsize=7.0, color=GRAY, va="center")
ax.text(6.92, 1.00, "第 16–18 层：颜色、光照", fontsize=7.0, color=GRAY, va="center")

ax.text(0.15, 0.58, "W：18 个风格层共用同一个 $w$，改一处，所有尺度一起变",
        fontsize=7.3, color=INK)
ax.text(0.15, 0.15, "W$^+$：每层各有一个 $w$，共 $18\\times512$ 维，深浅两层能分开改",
        fontsize=7.3, color=INK)

save(fig, "fig20_latent", CH)
