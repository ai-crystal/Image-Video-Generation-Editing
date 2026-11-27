import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"
a = 1.0
xs = np.linspace(-3, 3, 2001)

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25),
                         gridspec_kw=dict(wspace=0.30))

labels = [(1.0, RED, "$t=1$"), (0.5, BLUE, "$t=0.5$"), (0.25, GREEN, "$t=0.25$")]

ax = axes[0]
ax.axhline(a, color=LIGHT, lw=0.9, zorder=1)
ax.axhline(-a, color=LIGHT, lw=0.9, zorder=1)
for t, c, lab in labels:
    u = (1 - t) * a * xs / t ** 2
    ax.plot(xs, a * np.tanh(u), color=c, lw=1.5, label=lab, zorder=3)
ax.text(-2.95, a + 0.10, "真实样本 $+a$", fontsize=7.6, color=GRAY, ha="left")
ax.text(-2.95, -a - 0.26, "真实样本 $-a$", fontsize=7.6, color=GRAY, ha="left")
ax.text(0, 0, "", fontsize=1)
ax.annotate("整段压在均值上", (-0.9, 0.0), xytext=(-2.55, 0.30), fontsize=7.8,
            color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.set_xlim(-3, 3)
ax.set_ylim(-1.45, 1.45)
ax.set_xlabel("噪声点 $x_1$")
ax.set_ylabel(r"一步输出 $\hat{x}_0(x_1)$")
ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.30), fontsize=7.8, handlelength=1.4)
style(ax)

ax = axes[1]
for t, c, lab in labels:
    u = (1 - t) * a * xs / t ** 2
    err = a ** 2 / np.cosh(u) ** 2
    ax.plot(xs, err, color=c, lw=1.5, label=lab, zorder=3)
ax.axhline(a ** 2, color=GRAY, ls=(0, (4, 3)), lw=0.9, zorder=2)
ax.text(-2.95, a ** 2 + 0.10, "峰高 $a^2$，与 $t$ 无关", fontsize=7.8, color=GRAY)
ax.set_xlim(-3, 3)
ax.set_ylim(0, 1.32)
ax.set_xlabel("噪声点 $x_1$")
ax.set_ylabel(r"逐点均方误差 $E[(x_0-\hat{x}_0)^2\mid x_1]$")
ax.set_yticks([0, 0.5, 1.0])
style(ax, grid=True)

save(fig, "fig07_switch", CH)
