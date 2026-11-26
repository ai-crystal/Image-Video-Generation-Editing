import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "23"

# 一维玩具速度场 v(x, c) = a_c - x，源条件 a_s = 0，目标条件 a_t = 1
def v(x, a):
    return a - x

AS, AT = 0.0, 1.0
xs, xt = 2.0, 5.0

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.5), gridspec_kw=dict(wspace=0.22))


def arrow(ax, x0, dx, y, color, label):
    ax.annotate("", xy=(x0 + dx, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    ax.text(x0 + dx / 2.0, y + 0.14, label, color=color, fontsize=8.2,
            ha="center", va="bottom")


# 左：同点取差
ax = axes[0]
arrow(ax, xs, v(xs, AS), 0.0, GREEN, r"$v(x,c_s)$")
arrow(ax, xs, v(xs, AT), 0.55, BLUE, r"$v(x,c_t)$")
arrow(ax, xs, v(xs, AT) - v(xs, AS), 1.15, RED, r"方向 $=+1$")
ax.plot([xs], [0.0], "o", color=INK, ms=4)
ax.text(xs, -0.16, r"$x^s_t$", ha="center", va="top", fontsize=9)
ax.text(-1.05, 1.72, "(a)", fontsize=9.2, color=INK)

# 右：异点取差
ax2 = axes[1]
arrow(ax2, xs, v(xs, AS), 0.0, GREEN, r"$v(x^s,c_s)$")
arrow(ax2, xt, v(xt, AT), 0.55, BLUE, r"$v(x^t,c_t)$")
arrow(ax2, xt, v(xt, AT) - v(xs, AS), 1.15, RED, r"方向 $=-2$")
ax2.plot([xs], [0.0], "o", color=INK, ms=4)
ax2.plot([xt], [0.55], "o", color=INK, ms=4)
ax2.text(xs, -0.16, r"$x^s_t$", ha="center", va="top", fontsize=9)
ax2.text(xt, 0.42, r"$x^t_t$", ha="center", va="top", fontsize=9)
ax2.text(-1.05, 1.72, "(b)", fontsize=9.2, color=INK)

for ax in axes:
    ax.set_xlim(-1.2, 6.6)
    ax.set_ylim(-0.6, 1.85)
    ax.set_xlabel("状态空间位置 $x$")
    ax.set_yticks([])
    style(ax, spines=("top", "right", "left"))

save(fig, "fig23_cancel", CH)
