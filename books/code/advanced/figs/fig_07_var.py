import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"
fig, ax = plt.subplots(figsize=(W_HALF * 1.6, 2.2))

t = np.linspace(0, 1, 800)
v = t ** 2 / ((1 - t) ** 2 + t ** 2)

ax.plot(t, v, color=BLUE, lw=1.6, zorder=3)
for tt, dx, dy in [(0.1, 10, 16), (0.5, 0, 12), (0.9, -16, 6)]:
    vv = tt ** 2 / ((1 - tt) ** 2 + tt ** 2)
    ax.scatter([tt], [vv], s=18, c=BLUE, zorder=4)
    ax.annotate("%.2f" % vv, (tt, vv), xytext=(dx, dy), textcoords="offset points",
                fontsize=7.8, color=BLUE, ha="center")

ax.set_xlabel("噪声水平 $t$")
ax.set_ylabel(r"$\mathrm{Var}(x_0\mid x_t)\,/\,\sigma_d^2$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
style(ax, grid=True)
save(fig, "fig07_var", CH)
