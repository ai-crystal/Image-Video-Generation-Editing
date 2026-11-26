import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "11"

fig, ax = plt.subplots(figsize=(W_FULL, 2.75))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.6)
ax.axis("off")

QW, QH = 4.5, 0.78
QX = 0.5
AX0, AW = 6.3, 5.3


def box(x, y, w, h, text, fc="#f7f9fb", ec=GRAY, fs=7.0, style_="round,pad=0.02,rounding_size=0.08"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style_, fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=INK, linespacing=1.5)


questions = [
    "重建（强度置零）能还原原图吗",
    "整体结构对得上吗",
    "出错只发生在编辑区内吗",
    "编辑区是不是发灰、发软",
]
answers = [
    "问题在反演或表示\n调整步数、求解器、CFG",
    "问题在编辑方向或强度\n强度过大，低频被一起推走",
    "问题在条件与 mask\n区域没对齐，或方向向外扩散",
    "问题在高频\n平滑过强，或缺少低噪精修",
]
ys = [6.15, 4.75, 3.35, 1.95]

for i, (q, a, y) in enumerate(zip(questions, answers, ys)):
    box(QX, y, QW, QH, q, fc="#eef2f6", ec=BLUE, fs=7.0)
    box(AX0, y, AW, QH, a, fc="#fdfaf3", ec=SAND, fs=6.8)
    ax.annotate("", xy=(AX0 - 0.12, y + QH / 2), xytext=(QX + QW + 0.12, y + QH / 2),
                arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9))
    ax.text((QX + QW + AX0) / 2, y + QH / 2 + 0.16, "否", ha="center", fontsize=6.8, color=SAND)
    if i < len(questions) - 1:
        y2 = ys[i + 1] + QH
        ax.annotate("", xy=(QX + 1.6, y2 + 0.03), xytext=(QX + 1.6, y - 0.03),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9))
        ax.text(QX + 1.72, (y + y2) / 2, "是", ha="left", va="center", fontsize=6.8, color=BLUE)

box(QX, 0.55, QW, QH, "结果可用\n问题在语义强度，回到强度搜索", fc="#f2f6f2", ec=GREEN, fs=6.8)
ax.annotate("", xy=(QX + 1.6, 0.55 + QH + 0.03), xytext=(QX + 1.6, ys[-1] - 0.03),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9))
ax.text(QX + 1.72, (0.55 + QH + ys[-1]) / 2, "是", ha="left", va="center", fontsize=6.8, color=BLUE)

save(fig, "fig11_diag", CH)
