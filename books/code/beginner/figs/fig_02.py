import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
import matplotlib.patches as mpatches

CH = "02"

# ---------- 图 1.1 图像展平成向量 ----------
n = 96
yy, xx = np.mgrid[0:n, 0:n] / (n - 1.0)
img = 0.25 + 0.55 * (1 - yy) * (0.4 + 0.6 * xx)
img += 0.35 * ((xx - 0.32) ** 2 + (yy - 0.32) ** 2 < 0.035)
img -= 0.30 * ((xx - 0.72) ** 2 + (yy - 0.70) ** 2 < 0.05)
img = np.clip(img, 0, 1)

fig = plt.figure(figsize=(W_FULL, 2.5))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.35], height_ratios=[1, 1],
                      wspace=0.18, hspace=0.45)
ax0 = fig.add_subplot(gs[:, 0])
ax0.imshow(img, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
ax0.set_xticks([])
ax0.set_yticks([])
for s in ax0.spines.values():
    s.set_color("#8a8a8a")
    s.set_linewidth(0.6)
ax0.add_patch(mpatches.Rectangle((-0.5, -0.5), 31, 31, fill=False, ec=RED, lw=1.0))
ax0.add_patch(mpatches.Rectangle((63.5, 63.5), 31, 31, fill=False, ec=BLUE, lw=1.0))
ax0.text(15, -4, "前 32 行", color=RED, ha="center", va="bottom", fontsize=7.8)
ax0.text(79, n + 2, "后 32 行", color=BLUE, ha="center", va="top", fontsize=7.8)

ax1 = fig.add_subplot(gs[0, 1])
ax1.imshow(img.reshape(1, -1), cmap="gray", vmin=0, vmax=1, aspect="auto",
           interpolation="nearest", extent=(0, n * n, 0, 1))
ax1.set_ylim(0, 1.22)
ax1.set_yticks([])
ax1.set_xlabel("向量下标（行优先展开）", fontsize=8.4)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)
ax1.axvspan(0, 32 * n, color=RED, alpha=0.12, lw=0)
ax1.axvspan(n * n - 32 * n, n * n, color=BLUE, alpha=0.12, lw=0)
ax1.text(16 * n, 1.10, "0 … 3071", color=RED, ha="center", fontsize=7.8)
ax1.text(n * n - 16 * n, 1.10, "… 9215", color=BLUE, ha="center", fontsize=7.8)

ax2 = fig.add_subplot(gs[1, 1])
ax2.axis("off")
ax2.text(0.0, 0.78,
         "像素 $(i, j)$ 在向量里的位置是 $i \\cdot 96 + j$。\n"
         "相邻像素在向量里相邻，相邻两行隔着 96 个数。\n"
         "排列顺序不携带信息，信息在数值本身的关系里。",
         fontsize=8.6, color=INK, linespacing=2.0, va="top")
save(fig, "fig02_pixels", CH)

# ---------- 图 1.2 流形假设 ----------
t = np.linspace(-2.6, 2.6, 500)
curve = np.stack([t, 0.55 * np.sin(1.25 * t) + 0.16 * t], 1)
rng = np.random.default_rng(2)
pts = curve[rng.integers(0, len(curve), 260)] + rng.normal(0, 0.075, (260, 2))

A = curve[120] + np.array([0.02, 0.03])
B = curve[280] + np.array([-0.02, -0.02])
C = np.array([1.55, 1.30])

fig, ax = plt.subplots(figsize=(W_FULL, 2.55))
ax.plot(curve[:, 0], curve[:, 1], color=BLUE, lw=1.3, alpha=0.55)
ax.scatter(pts[:, 0], pts[:, 1], s=2.4, c=BLUE, alpha=0.55, lw=0)
ax.scatter(*C, s=28, c=RED, marker="x", lw=1.7)
ax.annotate("$A$（猫）", A, xytext=(A[0] - 0.95, A[1] + 0.85), fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
ax.annotate("$B$（另一只猫）", B, xytext=(B[0] - 0.15, B[1] - 0.95), fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
ax.annotate("$C$（随机噪声）", C, xytext=(C[0] - 1.55, C[1] + 0.35), fontsize=8.6, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
ax.plot([A[0], C[0]], [A[1], C[1]], ls=(0, (3, 3)), color=RED, lw=0.8)
ax.plot([A[0], B[0]], [A[1], B[1]], ls=(0, (3, 3)), color=GRAY, lw=0.8)
ax.set_xlim(-2.9, 2.9)
ax.set_ylim(-1.95, 2.0)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig02_manifold", CH)

# ---------- 图 1.3 质量与成本的权衡（定性示意） ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel("采样成本（网络前向次数）", fontsize=9)
ax.set_ylabel("生成质量", fontsize=9)

pts = [("对抗网络", 1.4, 6.2), ("一步蒸馏", 1.4, 7.4), ("扩散模型", 7.2, 8.3),
       ("变分自编码器", 1.4, 3.8)]
for name, x, y in pts:
    ax.scatter(x, y, s=42, c=BLUE, alpha=0.85, lw=0, zorder=3)
    ax.annotate(name, (x, y), xytext=(10, 0), textcoords="offset points",
                va="center", fontsize=9, color=INK)

ax.add_patch(plt.Rectangle((6.2, 7.6), 3.2, 1.4, fill=False, ec=SAND, lw=1.0, ls=(0, (4, 3))))
ax.annotate("", xy=(2.9, 7.55), xytext=(6.1, 8.15),
            arrowprops=dict(arrowstyle="-|>", color=SAND, lw=1.2,
                            connectionstyle="arc3,rad=0.18"))
ax.text(4.45, 8.62, "蒸馏：把多步压成一步", fontsize=8.4, color=SAND, ha="center")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right"))
ax.text(0.98, 0.04, "定性示意，不带具体数值", transform=ax.transAxes,
        ha="right", fontsize=8.0, color=GRAY)
save(fig, "fig02_tradeoff", CH)
