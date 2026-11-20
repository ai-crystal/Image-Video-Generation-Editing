import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "06"

# ---------- 图 5.1 四个噪声水平下的密度 ----------
centers = np.array([-1.6, 0.2, 1.7])
sig0 = 0.22
x = np.linspace(-4.5, 4.5, 800)


def mixture(x, s):
    out = np.zeros_like(x)
    for c in centers:
        out += np.exp(-(x - c) ** 2 / (2 * (sig0**2 + s**2))) / np.sqrt(2 * np.pi * (sig0**2 + s**2))
    return out / 3


fig, axes = plt.subplots(1, 4, figsize=(W_FULL, 1.8), sharey=True, gridspec_kw=dict(wspace=0.12))
for ax, s in zip(axes, [0.0, 0.35, 1.0, 2.4]):
    p = mixture(x, s)
    ax.fill_between(x, p, color=BLUE, alpha=0.25, lw=0)
    ax.plot(x, p, color=BLUE, lw=1.3)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 1.9)
    ax.set_yticks([])
    ax.set_xticks([-3, 0, 3])
    ax.set_xlabel("$x$", fontsize=8.4)
    ax.text(0.5, 0.92, "$\\sigma=%.2f$" % s, transform=ax.transAxes, ha="center",
            fontsize=8.0, color=GRAY)
    style(ax, spines=("top", "right"))
axes[0].set_ylabel("密度")
save(fig, "fig06_density", CH)

# ---------- 图 5.2 两种日程 ----------
T = 1000
beta_lin = np.linspace(1e-4, 0.02, T)
abar_lin = np.cumprod(1 - beta_lin)
s = 0.008
t = np.arange(1, T + 1) / T
abar_cos = np.cos((t + s) / (1 + s) * np.pi / 2) ** 2

fig, axes = plt.subplots(2, 1, figsize=(W_FULL, 2.9), sharex=True, gridspec_kw=dict(hspace=0.35))
ax = axes[0]
ax.plot(t, abar_lin, color=BLUE, lw=1.4, label="线性")
ax.plot(t, abar_cos, color=RED, lw=1.4, label="cosine")
ax.set_ylabel("$\\bar\\alpha_t$")
ax.legend(loc="lower left", fontsize=8.0)
style(ax, spines=("top", "right"))

ax = axes[1]
ax.semilogy(t, abar_lin / (1 - abar_lin + 1e-12), color=BLUE, lw=1.4)
ax.semilogy(t, abar_cos / (1 - abar_cos + 1e-12), color=RED, lw=1.4)
ax.set_ylabel("SNR")
ax.set_xlabel("$t/T$")
ax.set_ylim(1e-4, 1e4)
style(ax, spines=("top", "right"))
save(fig, "fig06_schedule", CH)
