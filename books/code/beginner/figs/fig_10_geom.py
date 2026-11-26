import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "10"

eu = np.array([0.10, -0.35])
ec = np.array([0.85, 0.15])
d = ec - eu

fig, ax = plt.subplots(figsize=(W_FULL * 0.60, 2.15))

# 两点连成的直线
s = np.linspace(-0.25, 2.05, 50)
line = eu[None, :] + s[:, None] * d[None, :]
ax.plot(line[:, 0], line[:, 1], color=LIGHT, lw=1.2, ls=(0, (4, 3)), zorder=1)

for w, col, lab, off in [(0.0, BLUE, "$w=0$", (0.06, -0.05)),
                         (1.0, GREEN, "$w=1$", (-0.34, 0.10)),
                         (1.8, RED, "$w=2$", (0.06, 0.10))]:
    p = eu + w * d
    ax.plot([p[0]], [p[1]], "o", ms=4.5, color=col, zorder=5)
    ax.text(p[0] + off[0], p[1] + off[1], lab, fontsize=8.4, color=col, zorder=6)

ax.annotate("", xy=eu, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2))
ax.annotate("", xy=ec, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))
ax.annotate("", xy=ec, xytext=eu,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))

ax.plot([0], [0], "o", ms=2.6, color=GRAY, zorder=6)
ax.text(-0.11, 0.02, "$0$", fontsize=8.0, color=GRAY, ha="center")
ax.text(0.20, -0.52, "$\\epsilon_{\\mathrm{uncond}}$", fontsize=8.4, color=BLUE)
ax.text(0.90, -0.05, "$\\epsilon_{\\mathrm{cond}}$", fontsize=8.4, color=GREEN)
ax.text(0.40, 0.04, "$\\Delta$", fontsize=8.8, color=RED)

p2 = eu + 1.8 * d
ax.annotate("", xy=p2, xytext=ec,
            arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=0.7,
                            shrinkA=7, shrinkB=7, ls=(0, (2, 2))))
ax.text(0.96, 0.56, "$(w-1)\\,|\\Delta|$", fontsize=7.9, color=GRAY)

ax.set_xlim(-0.25, 2.0)
ax.set_ylim(-0.75, 0.85)
ax.set_aspect("equal")
ax.axis("off")

save(fig, "fig10_geom", CH)
