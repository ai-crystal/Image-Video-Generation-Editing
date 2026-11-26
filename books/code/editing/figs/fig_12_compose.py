import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "12"

fig, ax = plt.subplots(figsize=(W_FULL, 2.45))
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 5.4)
ax.axis("off")

BW, BH = 2.05, 0.84
GAP = 0.40


def stage(x, y, text, fc="#f7f9fb", ec=GRAY, fs=6.6):
    ax.add_patch(FancyBboxPatch((x, y), BW, BH, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=0.8))
    ax.text(x + BW / 2, y + BH / 2, text, ha="center", va="center", fontsize=fs,
            color=INK, linespacing=1.6)


rows = [
    (4.25, ["原图", "反演 $z_T$", "条件去噪\nmask 约束", "输出"], "护住保真"),
    (3.00, ["原图", "反演 $z_T$", "改注意力\n仅 mask 内", "输出"], "护住对齐"),
    (1.75, ["原图", "加噪到 $t$", "一步\n加权速度差", "输出"], "护住稳定"),
    (0.50, ["原图\n降采样", "低分辨率\n编辑", "超分\n块间对齐", "输出"], "护住细节"),
]

for y, labels, note in rows:
    x = 0.40
    for i, lab in enumerate(labels):
        stage(x, y, lab, fc="#eef2f6" if i in (0, 3) else "#f7f9fb",
              ec=BLUE if i in (0, 3) else GRAY)
        if i < len(labels) - 1:
            ax.annotate("", xy=(x + BW + GAP - 0.04, y + BH / 2), xytext=(x + BW + 0.02, y + BH / 2),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
        x += BW + GAP
    ax.text(x + 0.35, y + BH / 2, note, ha="left", va="center", fontsize=7.2, color=SAND)

save(fig, "fig12_compose", CH)
