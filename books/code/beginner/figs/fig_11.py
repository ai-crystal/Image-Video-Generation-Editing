import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "09"
CH9 = "09"
CH10 = "10"

# ---------- 图 11.1 LDM 结构 ----------
fig, ax = plt.subplots(figsize=(W_FULL, 2.3))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")


def box(x, y, w, h, label, fc="#eef2f6", ec=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7.6, color=INK)


box(0.3, 2.5, 1.5, 1.1, "图像\n$512^2$")
box(2.4, 2.5, 1.6, 1.1, "编码器 $E$")
box(4.6, 2.5, 1.5, 1.1, "$z_0$\n$64^2$", fc="#fdf3e3", ec=SAND)
box(6.7, 2.5, 2.4, 1.1, "去噪网络\n(含 cross-attn)", fc="#e8eff6")
box(9.8, 2.5, 1.5, 1.1, "解码器 $D$")
box(6.9, 0.6, 2.0, 0.9, "文本编码器", fc="#f2f2f0", ec=GRAY)
for (x1, y1, x2, y2) in [(1.8, 3.05, 2.35, 3.05), (4.0, 3.05, 4.55, 3.05),
                          (6.1, 3.05, 6.65, 3.05), (9.1, 3.05, 9.75, 3.05)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(7.9, 2.45), xytext=(7.9, 1.55), arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9))
ax.text(6.0, 5.0, "像素空间", fontsize=7.4, color=GRAY)
ax.text(8.0, 5.0, "潜空间 diffusion", fontsize=7.4, color=GRAY)
ax.text(11.35, 3.05, "$x$", fontsize=8, va="center")
save(fig, "fig11_ldm", CH10)

# ---------- 图 11.2 cross-attention ----------
words = ["一只", "戴帽子的", "猫", "坐在", "草地上"]
grid = 8
A = np.zeros((len(words), grid, grid))
centers = [(2, 3), (2, 3), (2, 3), (5, 5), (6, 2)]
sigma = [(1.0, 1.2), (0.9, 0.9), (1.4, 1.3), (2.0, 1.6), (1.8, 2.2)]
for i, (cy, cx) in enumerate(centers):
    sy, sx = sigma[i]
    for r in range(grid):
        for c in range(grid):
            A[i, r, c] = np.exp(-((r - cy) ** 2 / (2 * sy ** 2) + (c - cx) ** 2 / (2 * sx ** 2)))
A /= A.sum(axis=(1, 2), keepdims=True)

fig, ax = plt.subplots(figsize=(W_FULL * 0.95, 2.35))
ax.set_xlim(0, 12.4)
ax.set_ylim(0, 8)
ax.axis("off")
for i, word in enumerate(words):
    ax.text(0.4, 7.2 - i * 1.25, word, fontsize=8, va="center")
    ax.annotate("", xy=(4.2, 6.6 - i * 1.25), xytext=(2.6, 7.2 - i * 1.25),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.8, alpha=0.8))
# 图像网格
for r in range(grid):
    for c in range(grid):
        w = A[2, r, c]
        ax.add_patch(plt.Rectangle((5.0 + c * 0.62, 6.6 - r * 0.62), 0.6, 0.6,
                                   fc=BLUE, alpha=0.05 + 0.9 * (w / A[2].max()) ** 0.7, ec="white", lw=0.6))
ax.text(7.6, 7.55, "图像 patch（$8\\times 8$）", fontsize=7.4, color=GRAY, ha="center")
ax.text(1.2, 7.75, "文本 token", fontsize=7.4, color=GRAY)
ax.text(10.6, 5.2, "注意力越亮，\n这个位置越\n关注“猫”", fontsize=7.6, color=INK, va="center")
save(fig, "fig11_attn", CH10)
