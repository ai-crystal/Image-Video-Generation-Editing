import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from math import sqrt

CH = "10"

mu, sd = 0.6, 0.12
x = np.linspace(0.0, 2.2, 600)


def normal(xx, m):
    return np.exp(-0.5 * ((xx - m) / sd) ** 2) / (sd * sqrt(2 * np.pi))


fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.4))

handles = []
for w, c in zip([1.0, 1.5, 2.0], [GREEN, SAND, RED]):
    m = w * mu
    ln, = ax.plot(x, normal(x, m), color=c, lw=1.4, label="$w=%g$" % w)
    handles.append(ln)
    xx = x[x >= 1.0]
    ax.fill_between(xx, normal(xx, m), color=c, alpha=0.15, lw=0)
    ax.plot([m], [normal(np.array([m]), m)[0]], "o", ms=3.0, color=c)

ax.axvline(1.0, color=GRAY, lw=0.8, ls=(0, (3, 3)))

ax.set_xlabel("某个像素通道的取值 $x$（虚线为像素上界）")
ax.set_ylabel("密度")
ax.set_xlim(0.0, 2.2)
ax.set_ylim(0, 3.7)
ax.set_yticks([])
ax.legend(handles=handles, loc="upper right", fontsize=7.8, labelspacing=0.3)
style(ax)

save(fig, "fig10_temper", CH)
