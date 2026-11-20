import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import Polygon

CH = "03"

# ---------- 图 2.1 二维高斯与条件分布 ----------
s1, s2, rho = 1.0, 0.75, 0.72
cov = np.array([[s1**2, rho * s1 * s2], [rho * s1 * s2, s2**2]])
inv = np.linalg.inv(cov)
gx, gy = np.mgrid[-3:3:240j, -3:3:240j]
pos = np.dstack([gx, gy])
dens = np.exp(-0.5 * np.einsum("...i,ij,...j->...", pos, inv, pos))

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3), gridspec_kw=dict(wspace=0.3))
ax = axes[0]
ax.contour(gx, gy, dens, levels=8, colors=[BLUE], linewidths=0.7, alpha=0.9)
ax.contourf(gx, gy, dens, levels=8, cmap="Blues", alpha=0.25)
x1 = 1.2
ax.axvline(x1, color=RED, lw=1.0)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
style(ax, spines=("top", "right"))

ax = axes[1]
m_cond = rho * s2 / s1 * x1
v_cond = s2**2 * (1 - rho**2)
yy = np.linspace(-2.5, 2.5, 400)
ax.plot(yy, np.exp(-(yy - m_cond) ** 2 / (2 * v_cond)) / np.sqrt(2 * np.pi * v_cond),
        color=RED, lw=1.4, label="条件密度")
ax.plot(yy, np.exp(-yy**2 / (2 * s2**2)) / np.sqrt(2 * np.pi * s2**2),
        color=GRAY, lw=1.0, ls=(0, (4, 3)), label="边缘密度")
ax.axvline(m_cond, color=RED, lw=0.6, ls=":")
ax.set_xlabel("$x_2$")
ax.set_ylabel("密度")
ax.legend(loc="upper left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig03_gauss", CH)

# ---------- 图 2.2 变量替换 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.62, 2.35))
J = np.array([[1.25, 0.55], [0.15, 0.85]])
sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
par = sq @ J.T
ax.add_patch(Polygon(sq, closed=True, fill=True, fc=BLUE, alpha=0.18, ec=BLUE, lw=1.2))
ax.add_patch(Polygon(par, closed=True, fill=True, fc=RED, alpha=0.16, ec=RED, lw=1.2))
ax.text(0.12, -0.26, "单位方格，面积 1", color=BLUE, fontsize=8.4)
ax.text(par[2, 0] + 0.06, par[2, 1] - 0.02, "映射后，面积 $|\\det J|$", color=RED, fontsize=8.4)
ax.set_xlim(-0.35, 2.5)
ax.set_ylim(-0.5, 1.6)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig03_jacobian", CH)

# ---------- 图 2.3 Jensen ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.62, 2.3))
x = np.linspace(-0.2, 2.4, 300)
f = x**2
x1p, x2p = 0.35, 1.95
ax.plot(x, f, color=BLUE, lw=1.5, label="$f(x)=x^2$")
ax.plot([x1p, x2p], [x1p**2, x2p**2], color=RED, lw=1.1, label="弦")
xm = (x1p + x2p) / 2
ax.scatter([xm], [xm**2], color=BLUE, s=24, zorder=4)
ax.scatter([xm], [(x1p**2 + x2p**2) / 2], color=RED, s=24, zorder=4)
ax.annotate("$f(E[X])$", (xm, xm**2), xytext=(xm + 0.12, xm**2 - 0.45),
            fontsize=8.2, color=BLUE, arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
ax.annotate("$E[f(X)]$", (xm, (x1p**2 + x2p**2) / 2), xytext=(xm + 0.14, (x1p**2 + x2p**2) / 2 + 0.18),
            fontsize=8.2, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.set_xlabel("$x$")
ax.set_ylabel("$f$")
ax.legend(loc="upper left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig03_jensen", CH)
