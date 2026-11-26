import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import Circle

CH = "19"

XL = (-1.5, 2.35)
YL = (-1.05, 1.95)
U = np.array([0.74, 0.67])
U = U / np.linalg.norm(U)
D = np.array([-U[1], U[0]])


def curve(t):
    return 0.34 + 0.52 * t - 0.15 * t ** 2


def panel(ax, r, thr, tag):
    ax.set_xlim(*XL)
    ax.set_ylim(*YL)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)

    # 保真约束
    ax.add_patch(Circle((0, 0), r, fc=BLUE, alpha=0.10, ec="none"))

    # 真实约束
    xs = np.linspace(XL[0] - 0.05, XL[1] + 0.05, 400)
    ax.plot(xs, curve(xs), color=GREEN, lw=6.0, alpha=0.15, solid_capstyle="butt")

    # 对齐约束的边界：只画视窗内的那一段
    p0 = thr * U
    ts = np.linspace(-8, 8, 4001)
    pts = p0[None, :] + ts[:, None] * D[None, :]
    inb = (pts[:, 0] > XL[0]) & (pts[:, 0] < XL[1]) & (pts[:, 1] > YL[0]) & (pts[:, 1] < YL[1])
    if inb.any():
        seg = pts[inb]
        ax.plot(seg[:, 0], seg[:, 1], color=RED, lw=1.0, ls=(0, (6, 4)))
        i = int(0.52 * (len(seg) - 1))
        ax.annotate("", xy=(seg[i, 0] + 0.42 * U[0], seg[i, 1] + 0.42 * U[1]),
                    xytext=(seg[i, 0], seg[i, 1]),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9, mutation_scale=7))

    # 三者的交集
    gx, gy = np.meshgrid(np.linspace(XL[0], XL[1], 200), np.linspace(YL[0], YL[1], 200))
    inside_ball = gx ** 2 + gy ** 2 <= r ** 2
    inside_half = gx * U[0] + gy * U[1] >= thr
    near_curve = np.abs(gy - curve(gx)) <= 0.085
    feas = inside_ball & inside_half & near_curve
    if feas.any():
        ax.contourf(gx, gy, feas.astype(float), levels=[0.5, 1.5], colors=[SAND], alpha=0.85)

    ax.scatter([0], [0], s=16, c=INK, zorder=6)
    ax.text(0.0, -0.20, "源图", fontsize=7.0, color=INK, ha="center", va="top")
    ax.text(XL[0] + 0.06, YL[1] - 0.12, tag, fontsize=8.0, color=GRAY, va="top")
    return feas.any()


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.28), gridspec_kw=dict(wspace=0.04))

f1 = panel(axes[0], 1.02, 0.46, "(a)")
axes[0].text(-0.86, 0.62, "保真", fontsize=7.2, color=BLUE, ha="center")
axes[0].text(1.62, 0.42, "真实", fontsize=7.2, color=GREEN, ha="center")
axes[0].text(1.42, -0.55, "对齐", fontsize=7.2, color=RED, ha="center")
axes[0].annotate("可行域很窄", xy=(0.66, 0.55), xytext=(0.05, 1.25), fontsize=7.2, color=SAND,
                 ha="left", arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.8,
                                            mutation_scale=6, connectionstyle="arc3,rad=0.2"))

f2 = panel(axes[1], 0.80, 1.00, "(b)")
axes[1].text(0.62, -0.95, "收紧阈值，交集为空", fontsize=7.2, color=GRAY, ha="center")

save(fig, "fig19_constraints", CH)
print("feasible a/b:", f1, f2)
