import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "09"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)
snr = abar / (1 - abar)
t = np.arange(T)


def weight(gamma):
    return np.minimum(snr, gamma)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.15),
                         gridspec_kw=dict(width_ratios=[1.45, 1.0], wspace=0.28))

ax = axes[0]
ax.loglog(t + 1, weight(np.inf), color=BLUE, lw=1.4, label="不截断（正比于 SNR）")
ax.loglog(t + 1, weight(5.0), color=RED, lw=1.4, label="$\\gamma=5$")
ax.loglog(t + 1, weight(1.0), color=GREEN, lw=1.4, label="$\\gamma=1$")
ax.axhline(5.0, color=RED, lw=0.7, ls=(0, (4, 3)), alpha=0.6)
ax.text(1.6, 6.4, "$\\gamma$", color=RED, fontsize=8.0)
ax.annotate("$t\\approx130$", xy=(130, 5.0), xytext=(180, 60), fontsize=7.8, color=GRAY,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.set_xlabel("训练步 $t$")
ax.set_ylabel("每步权重")
ax.set_xlim(1, T)
ax.set_ylim(1e-5, 3e4)
ax.legend(loc="lower left", fontsize=7.8)
style(ax, grid=True)

ax = axes[1]
labels = ["无截断", "$\\gamma=20$", "$\\gamma=5$", "$\\gamma=1$"]
gammas = [np.inf, 20.0, 5.0, 1.0]
frac = []
for g in gammas:
    w = weight(g)
    frac.append(w[:100].sum() / w.sum())
colors = [BLUE, PURPLE, RED, GREEN]
bars = ax.barh(np.arange(4), frac, height=0.55, color=colors, alpha=0.85)
for i, f in enumerate(frac):
    ax.text(f + 0.02, i, "%.0f%%" % (100 * f), va="center", fontsize=8.0, color=INK)
ax.set_yticks(np.arange(4))
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlim(0, 1.25)
ax.set_xlabel("前 100 步占的权重比例")
style(ax)

save(fig, "fig09_minsnr", CH)
