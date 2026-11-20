import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ---------- 图 12.1 数据量 ----------
CH = "12"
sizes = [
    ("单张 512² 图", 3 * 512 * 512),
    ("1 秒 24 帧", 24 * 3 * 512 * 512),
    ("5 秒 120 帧", 120 * 3 * 512 * 512),
    ("潜空间 5 秒\n(16×64×64×30)", 16 * 64 * 64 * 30),
]
fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.2))
names = [s[0] for s in sizes]
vals = [s[1] for s in sizes]
colors = [BLUE, BLUE, BLUE, GREEN]
bars = ax.bar(range(len(vals)), vals, color=colors, width=0.55, alpha=0.9)
ax.set_yscale("log")
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(names, fontsize=7.8)
ax.set_ylabel("数值个数（对数）")
for i, v in enumerate(vals):
    ax.text(i, v * 1.5, "%.0e" % v if v >= 1e6 else "%.1e" % v, ha="center", fontsize=7.6, color=INK)
ax.set_ylim(1e5, 5e8)
style(ax, spines=("top", "right"))
ax.grid(True, axis="y", which="major", color=LIGHT, lw=0.5, alpha=0.8)
ax.set_axisbelow(True)
save(fig, "fig12_size", CH)

# ---------- 图 13.1 两种时空注意力 ----------
CH = "13"
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3), gridspec_kw=dict(wspace=0.18))


def frame(ax, x0, y0, n=3, cell=0.3, fc="#f7f9fb", alpha=1.0, ec=BLUE_L, z=2):
    for i in range(n):
        for j in range(n):
            ax.add_patch(plt.Rectangle((x0 + j * cell, y0 + i * cell), cell, cell,
                                       fc=fc, ec=ec, lw=0.5, alpha=alpha, zorder=z))


def stack(ax):
    for k, x0 in enumerate([0.0, 1.35, 2.7]):
        frame(ax, x0, 0.0)
        ax.text(x0 + 0.45, -0.22, "帧 %d" % (k + 1), ha="center", fontsize=6.8, color=GRAY)
    ax.set_xlim(-0.15, 4.2)
    ax.set_ylim(-0.45, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")


ax = axes[0]
stack(ax)
for x0 in [0.0, 1.35, 2.7]:
    frame(ax, x0, 0.0, fc=BLUE, alpha=0.16, ec="none", z=5)
q = (1.35 + 0.45, 0.45)
for c in [(0.45, 0.15), (0.45, 0.75), (3.15, 0.15), (3.15, 0.75)]:
    ax.plot([q[0], c[0]], [q[1], c[1]], color=BLUE, lw=0.8, ls=(0, (3, 2)), zorder=6)
ax.scatter([q[0]], [q[1]], s=26, c=RED, zorder=7)

ax = axes[1]
stack(ax)
frame(ax, 1.35, 0.0, fc=BLUE, alpha=0.22, ec="none", z=5)
for x0 in [0.0, 1.35, 2.7]:
    ax.add_patch(plt.Rectangle((x0 + 0.3, 0.3), 0.3, 0.3, fc=GREEN, alpha=0.45, ec="none", zorder=6))
ax.annotate("", xy=(2.85, 0.45), xytext=(0.15, 0.45),
            arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.0, zorder=7))
ax.set_xlim(-0.15, 4.2)
ax.set_ylim(-0.45, 1.35)
ax.set_aspect("equal")
ax.axis("off")
save(fig, "fig13_attention", CH)

# ---------- 图 14.1 时间层插入 ----------
CH = "14"
fig, ax = plt.subplots(figsize=(W_FULL, 2.15))
ax.set_xlim(0, 11.4)
ax.set_ylim(0, 4.6)
ax.axis("off")


def cell(x, y, label, frozen=False):
    ax.add_patch(FancyBboxPatch((x, y), 2.2, 0.85, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#f4f4f2" if frozen else "#e8eff6",
                                ec=GRAY if frozen else BLUE, lw=0.9,
                                ls=(0, (3, 2)) if frozen else "-"))
    ax.text(x + 1.1, y + 0.42, label, ha="center", va="center", fontsize=7.0, color=INK)


for k in range(3):
    x = 0.9 + k * 3.4
    cell(x, 2.55, "空间层（冻结）", frozen=True)
    cell(x, 1.05, "时间层（训练）", frozen=False)
    ax.annotate("", xy=(x + 1.1, 2.45), xytext=(x + 1.1, 1.95),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
    if k < 2:
        ax.annotate("", xy=(x + 3.35, 1.47), xytext=(x + 2.35, 1.47),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
        ax.annotate("", xy=(x + 3.35, 2.97), xytext=(x + 2.35, 2.97),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
save(fig, "fig14_temporal", CH)

# ---------- 图 15.1 3D VAE ----------
CH = "15"
fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.15))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4.6)
ax.axis("off")
for k in range(4):
    ax.add_patch(FancyBboxPatch((0.8 + 0.35 * k, 0.9 + 0.3 * k), 1.6, 1.6,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                fc="#eef2f6", ec=BLUE, lw=0.8, alpha=0.9))
ax.text(2.1, 0.45, "视频 $T\\times C\\times H\\times W$", fontsize=7.4, ha="center")
ax.annotate("", xy=(6.0, 2.3), xytext=(4.2, 2.3),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.0))
ax.text(5.1, 2.5, "空间 ÷8\n时间 ÷4", fontsize=6.9, ha="center", color=GRAY, linespacing=1.5)
for k in range(3):
    ax.add_patch(FancyBboxPatch((7.0 + 0.35 * k, 1.5 + 0.3 * k), 0.7, 0.7,
                                boxstyle="round,pad=0.02,rounding_size=0.04",
                                fc="#eef5f0", ec=GREEN, lw=0.8))
ax.text(8.3, 0.45, "潜变量 $t\\times c\\times h\\times w$", fontsize=7.4, ha="center")
ax.text(9.6, 2.3, "时间上压缩得越多，\n节省越大，快速运动越容易糊", fontsize=6.9,
        color=GRAY, va="center", ha="center", linespacing=1.6)
save(fig, "fig15_vae", CH)

# ---------- 图 16.1 长视频两种策略 ----------
CH = "16"
fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.45))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.6)
ax.axis("off")
# 分块
for i in range(4):
    x = 0.6 + i * 2.6
    ax.add_patch(FancyBboxPatch((x, 3.3), 2.2, 0.9, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#eef2f6", ec=BLUE, lw=0.8))
    ax.text(x + 1.1, 3.75, "块 %d" % (i + 1), ha="center", va="center", fontsize=7.0)
    if i < 3:
        ax.annotate("", xy=(x + 2.55, 3.75), xytext=(x + 2.25, 3.75),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
    if i > 0:
        ax.annotate("", xy=(x + 0.15, 3.3), xytext=(x - 0.05, 3.75),
                    arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.7, ls=(0, (3, 2))))
ax.text(6.0, 4.55, "分块自回归：前一块的末帧作为下一块的条件", fontsize=7.2, color=GRAY, ha="center")

# 层次
for i in range(3):
    x = 0.9 + i * 3.6
    ax.add_patch(FancyBboxPatch((x, 1.2), 2.0, 0.8, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#eef5f0", ec=GREEN, lw=0.8))
    ax.text(x + 1.0, 1.6, "关键帧", ha="center", va="center", fontsize=7.0)
    if i < 2:
        ax.annotate("", xy=(x + 3.4, 1.6), xytext=(x + 2.1, 1.6),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
ax.text(6.0, 2.35, "层次生成：先生成关键帧，再插帧补细节", fontsize=7.2, color=GRAY, ha="center")
save(fig, "fig16_long", CH)

# ---------- 图 24.1 逐帧闪烁与一致 ----------
CH = "24"
rng = np.random.default_rng(5)
fig, ax = plt.subplots(figsize=(W_FULL, 2.05))
ax.set_xlim(-0.2, 9.4)
ax.set_ylim(-0.25, 3.3)
ax.axis("off")

for row, y0, jitter in [(0, 2.0, 0.18), (1, 0.45, 0.0)]:
    for k in range(4):
        base = 0.62 + (rng.normal(0, jitter) if jitter else 0.0)
        ax.add_patch(plt.Rectangle((k * 2.2, y0), 1.7, 1.0,
                                   fc=(base, base * 0.96, base * 0.92), ec=LIGHT, lw=0.6))
        cx = k * 2.2 + 0.55 + 0.18 * k
        ax.add_patch(plt.Circle((cx, y0 + 0.5), 0.13, color=BLUE, alpha=0.9))
        ax.text(k * 2.2 + 0.85, y0 - 0.16, "帧 %d" % (k + 1), ha="center", fontsize=6.8, color=GRAY)
save(fig, "fig24_flicker", CH)
