import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ---------- 图 9.1 三种对应关系 ----------
CH = "09"
fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.85), gridspec_kw=dict(wspace=0.12))
titles = []
for ax in axes:
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")

# 光流
ax = axes[0]
ax.add_patch(plt.Rectangle((0.2, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
ax.add_patch(plt.Rectangle((2.1, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
rng = np.random.default_rng(1)
for i in range(5):
    for j in range(6):
        x = 0.45 + i * 0.32
        y = 0.5 + j * 0.28
        ax.annotate("", xy=(2.35 + i * 0.32, y), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.5, alpha=0.8))
ax.text(1.05, -0.05, "帧 $t$", ha="center", fontsize=7.0, color=GRAY)
ax.text(2.95, -0.05, "帧 $t+1$", ha="center", fontsize=7.0, color=GRAY)

# 轨迹
ax = axes[1]
ax.add_patch(plt.Rectangle((0.2, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
ax.add_patch(plt.Rectangle((2.1, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
pts0 = [(0.7, 0.8), (1.2, 1.4), (1.6, 0.7)]
pts1 = [(2.6, 0.95), (3.1, 1.5), (3.45, 0.85)]
for a, b in zip(pts0, pts1):
    ax.plot([a[0] + 2.0, b[0]], [a[1], b[1]], color=GREEN, lw=1.0)
    ax.scatter([a[0]], [a[1]], s=16, color=GREEN, zorder=4)
    ax.scatter([b[0]], [b[1]], s=16, color=GREEN, zorder=4)
ax.text(1.05, -0.05, "帧 $t$", ha="center", fontsize=7.0, color=GRAY)
ax.text(2.95, -0.05, "帧 $t+1$", ha="center", fontsize=7.0, color=GRAY)

# 特征对应
ax = axes[2]
ax.add_patch(plt.Rectangle((0.2, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
ax.add_patch(plt.Rectangle((2.1, 0.3), 1.7, 1.8, fc="#f7f9fb", ec=BLUE_L, lw=0.7))
for k in range(4):
    y0 = 0.55 + k * 0.38
    ax.plot([1.1, 2.7], [y0 + 0.05, y0 + 0.28], color=PURPLE, lw=0.7, ls=(0, (3, 2)))
    ax.scatter([1.1], [y0 + 0.05], s=14, color=PURPLE, zorder=4)
    ax.scatter([2.7], [y0 + 0.28], s=14, color=PURPLE, zorder=4)
ax.text(1.05, -0.05, "帧 $t$", ha="center", fontsize=7.0, color=GRAY)
ax.text(2.95, -0.05, "帧 $t+1$", ha="center", fontsize=7.0, color=GRAY)
save(fig, "fig09_corr", CH)

# ---------- 图 10.1 三类流程 ----------
CH = "10"
fig, ax = plt.subplots(figsize=(W_FULL, 2.15))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4.6)
ax.axis("off")


def box(x, y, w, h, label, fc, ec, fs=7.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK,
            linespacing=1.4)


rows = [
    (3.35, ["输入视频", "编辑关键帧", "光流传播", "输出视频"], "传播"),
    (1.85, ["输入视频", "分解内容/运动", "编辑内容", "重渲染"], "形变"),
    (0.35, ["输入视频", "编码进视频模型", "整体生成", "输出视频"], "整体"),
]
for y, labels, tag in rows:
    x = 0.35
    for i, lab in enumerate(labels):
        fc = "#eef2f6" if i in (0, 3) else "#f7f9fb"
        box(x, y, 2.2, 0.85, lab, fc, BLUE if i in (0, 3) else GRAY)
        if i < len(labels) - 1:
            ax.annotate("", xy=(x + 2.75, y + 0.42), xytext=(x + 2.25, y + 0.42),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
        x += 2.9
    ax.text(0.35, y + 1.02, tag, fontsize=6.8, color=GRAY)
save(fig, "fig10_routes", CH)
