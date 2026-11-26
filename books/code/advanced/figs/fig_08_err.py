import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "08"
fig, ax = plt.subplots(figsize=(W_HALF * 1.62, 2.2))

d = np.linspace(0.005, 0.5, 600)
for a, c, lab in [(1.0, BLUE, "$a=1$"), (3.0, GREEN, "$a=3$"), (10.0, RED, "$a=10$")]:
    err = np.abs((1 - a * d) * np.exp(a * d) - 1)
    err = np.maximum(err, 1e-6)
    ax.semilogy(d, err, color=c, lw=1.5, label=lab)

ax.scatter([0.1], [1.0], s=24, c=RED, zorder=5)

ax.set_xlabel(r"单步间隔 $\Delta$")
ax.set_ylabel("相对一致性误差")
ax.set_xlim(0, 0.5)
ax.set_ylim(1e-4, 1e2)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0, 1, 0.12), ncol=3,
          mode="expand", borderaxespad=0.0)
style(ax, grid=True)
save(fig, "fig08_err", CH)
