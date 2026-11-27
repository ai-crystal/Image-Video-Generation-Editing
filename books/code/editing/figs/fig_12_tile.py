import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "12"

# 一维剖面上的分块权重叠加：S=1536, 块长 512, 重叠 128, 步长 384
S, L, O = 1536, 512, 128
stride = L - O
starts = list(range(0, S - L + 1, stride))
if starts[-1] != S - L:
    starts.append(S - L)


def window(u):
    """块内坐标 u 处的余弦窗权重：两端各 O 像素的升余弦过渡，中段为 1。"""
    w = np.ones_like(u)
    w = np.where(u < O, np.sin(np.pi * u / (2 * O)) ** 2, w)
    w = np.where(u > L - O, np.cos(np.pi * (u - (L - O)) / (2 * O)) ** 2, w)
    return w


x = np.arange(S, dtype=float)
tot = np.zeros(S)
for s in starts:
    u = x - s
    m = (u >= 0) & (u <= L)
    tot[m] += window(u[m])

fig, ax = plt.subplots(figsize=(W_FULL, 1.95))
ax.axhspan(0, 2.6, xmin=(1024 / S), xmax=(1280 / S), color=LIGHT, alpha=0.55, lw=0)
ax.plot(x, tot, lw=1.6, color=BLUE)
ax.axhline(1.0, lw=0.9, ls=(0, (4, 2)), color=GRAY)

ax.annotate("最后一块贴边放置\n重叠带变成 256，权重和升到 2",
            xy=(1160, 1.98), xytext=(1215, 2.45),
            fontsize=6.4, color=RED, ha="center", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.7,
                            connectionstyle="angle,angleA=0,angleB=90,rad=0"))
ax.annotate("块边缘权重从 0 起",
            xy=(6, 0.06), xytext=(150, 0.30),
            fontsize=6.4, color=GRAY, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
ax.text(760, 1.13, "中间带：只被一块覆盖", fontsize=6.4, color=GRAY, va="bottom", ha="center")

ax.set_xlim(0, S)
ax.set_ylim(0, 2.65)
ax.set_xlabel("像素坐标（$S=1536$，四块起点 $0/384/768/1024$）")
ax.set_ylabel(r"权重和 $\sum_i w_i$")
ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
style(ax, grid=False)
save(fig, "fig12_tile", CH)
