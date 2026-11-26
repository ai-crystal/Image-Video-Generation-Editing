import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "06"

# ---------- 图 6.2 典型集厚度随维度下降 ----------
d = np.logspace(2, 6, 300)
rel = np.sqrt(2.0 / d)
fig, ax = plt.subplots(figsize=(W_FULL * 0.76, 2.1))
ax.plot(d, 100 * rel, color=BLUE, lw=1.5)
for dd, txt, off in [(4096, "$2.2\\%$", (8, 16)),
                    (16384, "$1.1\\%$", (0, 14)),
                    (65536, "$0.55\\%$", (6, 22))]:
    ax.plot([dd], [100 * np.sqrt(2.0 / dd)], "o", ms=4.5, color=RED, zorder=5)
    ax.annotate(txt, xy=(dd, 100 * np.sqrt(2.0 / dd)), xytext=off, textcoords="offset points",
                fontsize=7.6, color=INK)
ax.set_xscale("log")
ax.set_xlim(1e2, 3e6)
ax.set_xlabel("潜变量维度 $d$")
ax.set_ylabel("典型球壳的相对厚度（%）")
ax.set_ylim(0, 15)
style(ax, spines=("top", "right"))
save(fig, "fig06_typical", CH)

# ---------- 图 6.3 有限 lambda 的受控轨迹 ----------
y0, y1 = 0.2, -0.6
tt = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(W_FULL * 0.76, 2.15))
for lam, c, lab in [(0.5, GRAY, "$\\lambda=0.5$"), (1.0, SAND, "$\\lambda=1$"),
                    (4.0, PURPLE, "$\\lambda=4$")]:
    z = y1 - (y1 - y0) * (1 - tt + 1 / lam) / (1 + 1 / lam)
    ax.plot(tt, z, color=c, lw=1.4, label=lab + "，残差 %.2f" % (abs(y1 - y0) / (1 + lam)))
ax.axhline(y1, color=BLUE, lw=1.0, ls=(0, (4, 3)))
ax.text(0.60, y1 + 0.035, "$y_1=-0.6$：目标终点", fontsize=7.8, color=BLUE)
ax.plot([0], [y0], "o", ms=4.5, color=INK, zorder=5)
ax.text(0.01, y0 + 0.04, "$y_0=0.2$", fontsize=7.8, color=INK)
ax.set_xlabel("$t$")
ax.set_ylabel("$z_t$（一维）")
ax.set_ylim(-0.75, 0.35)
ax.legend(loc="lower left", fontsize=7.6)
style(ax, spines=("top", "right"))
save(fig, "fig06_lqr", CH)
