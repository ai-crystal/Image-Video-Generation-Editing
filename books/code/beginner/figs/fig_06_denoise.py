import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "06"

centers = np.array([-1.5, 1.5])
sig0 = 0.30


def xhat(x, s):
    """两峰混合数据的后验均值 E[x0 | x_t = x]，噪声水平为 s。"""
    v = sig0**2 + s**2
    num = np.zeros_like(x)
    den = np.zeros_like(x)
    for c in centers:
        g = np.exp(-(x - c) ** 2 / (2 * v))
        num += g * c
        den += g
    return num / den


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25),
                         gridspec_kw=dict(width_ratios=[1.3, 0.9], wspace=0.32))

ax = axes[0]
x = np.linspace(-4, 4, 1200)
for s, c in [(0.12, RED), (0.45, SAND), (1.20, BLUE)]:
    ax.plot(x, xhat(x, s), color=c, lw=1.5, label="$\\sigma=%.2f$" % s)
for c in centers:
    ax.plot([c], [c], marker="o", ms=3.0, color=GRAY)
ax.axhline(0, color=LIGHT, lw=0.8)
ax.set_xlabel("含噪输入 $x_t$")
ax.set_ylabel("最优去噪 $\\hat{x}_\\sigma(x_t)$")
ax.set_yticks([-1.5, 0, 1.5])
ax.legend(loc="lower right", fontsize=7.6)
style(ax)

ax = axes[1]
ss = np.geomspace(0.03, 1.5, 70)
slope = []
for s in ss:
    g = np.gradient(xhat(x, s), x)
    slope.append(np.max(np.abs(g)))
ax.loglog(ss, slope, color=BLUE, lw=1.5, label="最大斜率")
ax.loglog(ss, 2.2 / (sig0**2 + ss**2), color=GRAY, lw=0.9, ls=(0, (4, 3)),
          label="$\\propto 1/(\\sigma_0^2+\\sigma^2)$")
ax.set_xlabel("噪声水平 $\\sigma$")
ax.set_ylabel("$\\max|\\mathrm{d}\\hat{x}/\\mathrm{d}x|$")
ax.legend(loc="lower left", fontsize=7.4)
style(ax)
save(fig, "fig06_denoise", CH)
