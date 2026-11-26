import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "03"

V = 2.0
SIG = 0.7


def f(x, t):
    return np.exp(-(x - V * t) ** 2 / (2 * SIG**2))


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.32))

# ---------- 左：三个时刻的场 ----------
ax = axes[0]
x = np.linspace(-1.0, 6.0, 600)
for t, c, ls in [(0.0, BLUE, "-"), (1.0, BLUE_L, "-"), (2.0, RED, "-")]:
    ax.plot(x, f(x, t), color=c, lw=1.4, ls=ls, label="$t=%d$" % t)
ax.plot([0.0], [f(0.0, 0.0)], "o", ms=4, color=INK, zorder=5)
ax.annotate("$(x,t)=(0,0)$", (0.0, 1.0), xytext=(0.35, 1.16), fontsize=7.6,
            color=INK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.set_xlabel("$x$")
ax.set_ylabel("$f(x,t)$")
ax.set_ylim(0, 1.42)
ax.set_yticks([0, 0.5, 1.0])
ax.legend(loc="upper right", fontsize=7.6)
style(ax, spines=("top", "right"))

# ---------- 右：时空图与轨迹 ----------
ax = axes[1]
tt, xx = np.mgrid[0:2:200j, -1:6:320j]
F = f(xx, tt)
ax.contourf(xx, tt, F, levels=10, cmap="Blues", alpha=0.55)
ax.contour(xx, tt, F, levels=[0.5], colors=[BLUE], linewidths=0.8)
tline = np.linspace(0, 2, 60)
ax.plot(V * tline + 0.5, tline, color=RED, lw=1.3)
for t in (0.0, 1.0, 2.0):
    ax.plot(V * t + 0.5, t, "o", ms=3.6, color=RED, zorder=5)
ax.annotate("沿这条线\n$f$ 不变", (V * 1.0 + 0.5, 1.0), xytext=(0.05, 1.42),
            fontsize=7.4, color=RED, linespacing=1.6, va="center",
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.set_xlabel("$x$")
ax.set_ylabel("$t$")
ax.set_xlim(-1, 6)
ax.set_ylim(0, 2)
style(ax, spines=("top", "right"))

save(fig, "fig03_advect", CH)
