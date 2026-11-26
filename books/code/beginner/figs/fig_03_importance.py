import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "03"


def norm(x, s):
    return np.exp(-x**2 / (2 * s**2)) / (np.sqrt(2 * np.pi) * s)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.34))

# ---------- 左：p 与更窄的 q ----------
ax = axes[0]
x = np.linspace(-5, 5, 700)
s_q = 0.74
ax.plot(x, norm(x, 1.0), color=BLUE, lw=1.5, label="$p=\\mathcal{N}(0,1)$")
ax.plot(x, norm(x, s_q), color=RED, lw=1.3, label="$q=\\mathcal{N}(0,0.74^2)$")
ax.fill_between(x, norm(x, s_q), color=RED, alpha=0.10, lw=0)
ax.set_xlabel("$x$")
ax.set_ylabel("密度")
ax.set_xlim(-5, 5)
ax.set_yticks([])
ax.legend(loc="upper left", fontsize=7.8)
ax.text(2.35, 0.085, "尾部 q 比 p 薄\n权重在这里爆炸", fontsize=7.6, color=RED,
        ha="left", va="bottom", linespacing=1.6)
style(ax, spines=("top", "right"))

# ---------- 右：方差随提议分布宽度的变化 ----------
ax = axes[1]
s = np.linspace(0.7085, 3.0, 800)
var = s / np.sqrt(2 - 1 / s**2) - 1
ax.semilogy(s, np.clip(var, 1e-3, 40), color=BLUE, lw=1.5)
ax.axvline(1 / np.sqrt(2), color=RED, lw=0.9, ls=(0, (4, 3)))
ax.text(1 / np.sqrt(2) + 0.07, 3.2, "方差发散\n  $\\sigma\\to 1/\\sqrt{2}$", fontsize=7.6,
        color=RED, linespacing=1.6, va="center")
ax.scatter([1.0], [1e-3], s=14, color=GREEN, zorder=4)
ax.annotate("$\\sigma=1$\n方差为零", (1.0, 1e-3), xytext=(1.25, 0.012),
            fontsize=7.6, color=GREEN, linespacing=1.6,
            arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6))
ax.set_xlabel("提议分布宽度 $\\sigma$")
ax.set_ylabel("$\\mathrm{Var}_q[w]$")
ax.set_xlim(0.70, 3.0)
ax.set_ylim(1e-3, 20)
ax.set_yticks([1e-3, 1e-1, 1e1])
style(ax, spines=("top", "right"))

save(fig, "fig03_importance", CH)
