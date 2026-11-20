import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

CH = "04"

# ---------- 图 3.1 自编码器与隐空间空洞 ----------
fig = plt.figure(figsize=(W_FULL, 2.35))
ax = fig.add_axes([0.0, 0.0, 0.46, 1.0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


def box(x, y, w, h, label, fc="#eef2f6", ec=BLUE, size=8.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.008,rounding_size=0.02",
                                fc=fc, ec=ec, lw=0.9, transform=ax.transAxes))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size,
            color=INK, transform=ax.transAxes, linespacing=1.6)


box(0.02, 0.55, 0.19, 0.26, "图像\n$x$")
box(0.31, 0.50, 0.26, 0.36, "编码器\n$f_\\phi$", fc="#e8eff6")
box(0.68, 0.58, 0.13, 0.20, "$z$", fc="#fdf3e3", ec=SAND)
box(0.31, 0.12, 0.26, 0.26, "解码器\n$g_\\theta$", fc="#e8eff6")
box(0.02, 0.10, 0.19, 0.26, "重构\n$\\hat{x}$")

for (x1, y1, x2, y2) in [(0.215, 0.68, 0.305, 0.68), (0.575, 0.68, 0.675, 0.68),
                          (0.675, 0.60, 0.575, 0.60),
                          (0.305, 0.25, 0.215, 0.25)]:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9,
                                 color=GRAY, lw=0.9, shrinkA=0, shrinkB=0,
                                 transform=ax.transAxes))

ax2 = fig.add_axes([0.52, 0.16, 0.44, 0.76])
rng = np.random.default_rng(5)
centers = np.array([[-1.35, 0.85], [1.05, 1.15], [-0.95, -1.15], [1.45, -0.75], [0.15, 1.85]])
pts = np.vstack([c + rng.normal(0, 0.15, (24, 2)) for c in centers])
ax2.scatter(pts[:, 0], pts[:, 1], s=3.4, c=BLUE, alpha=0.75, lw=0)
ax2.scatter(0.0, 0.0, s=26, c=RED, marker="x", lw=1.5, zorder=4)
ax2.text(0.18, -0.62, "解码这个点\n得到无意义的图", fontsize=7.8, color=RED,
         ha="left", va="top", linespacing=1.6)
ax2.annotate("", xy=(0.03, -0.12), xytext=(0.16, -0.55),
             arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax2.set_xlabel("$z_1$")
ax2.set_ylabel("$z_2$")
ax2.set_xlim(-2.1, 2.2)
ax2.set_ylim(-2.1, 2.3)
ax2.set_xticks([])
ax2.set_yticks([])
style(ax2, spines=("top", "right"))
save(fig, "fig04_ae", CH)

# ---------- 图 3.2 条件多峰与均方误差 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.4))
x = np.linspace(0, 1, 500)
p1 = np.exp(-((x - 0.28) ** 2) / (2 * 0.055 ** 2))
p2 = np.exp(-((x - 0.72) ** 2) / (2 * 0.055 ** 2))
p = 0.5 * p1 + 0.5 * p2
ax.fill_between(x, p, color=BLUE, alpha=0.16, lw=0)
ax.plot(x, p, color=BLUE, lw=1.4, label="$p(x\\,|\\,z)$")
ax.axvline(0.5, color=RED, lw=1.1, ls=(0, (4, 3)), label="均方误差最优解")
ax.annotate("可能是深色", (0.28, 1.0), xytext=(0.03, 1.18), fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.annotate("也可能是浅色", (0.72, 1.0), xytext=(0.76, 1.18), fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.set_xlabel("像素强度")
ax.set_ylabel("密度")
ax.set_ylim(0, 1.42)
ax.set_yticks([])
ax.legend(loc="upper left", fontsize=7.8)
ax.text(0.5, 0.26, "回归到均值，输出灰色", transform=ax.transAxes, ha="center",
        fontsize=8.2, color=RED)
style(ax, spines=("top", "right"))
save(fig, "fig04_blur", CH)
