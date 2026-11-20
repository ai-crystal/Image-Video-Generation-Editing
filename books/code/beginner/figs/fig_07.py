import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
alpha = 1 - beta
abar = np.cumprod(alpha)
w = (1 - alpha) ** 2 / (2 * alpha * (1 - abar))

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.2), gridspec_kw=dict(wspace=0.32))
ax = axes[0]
ax.semilogy(np.arange(1, T + 1), w, color=BLUE, lw=1.4)
ax.set_xlabel("$t$")
ax.set_ylabel("权重")
style(ax, spines=("top", "right"))

ax = axes[1]
ax.plot(np.arange(1, T + 1), w / w.sum() * T, color=BLUE, lw=1.4, label="加权损失")
ax.axhline(1.0, color=RED, lw=1.1, ls=(0, (4, 3)), label="等权重")
ax.set_xlabel("$t$")
ax.set_ylabel("相对权重")
ax.set_yscale("log")
ax.legend(loc="upper right", fontsize=7.8)
style(ax, spines=("top", "right"))
save(fig, "fig07_weight", CH)
