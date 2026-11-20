import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "05"

# ---------- 图 4.1 JS 散度饱和 ----------
d = np.linspace(0, 8, 300)
sigma = 1.0
js = np.zeros_like(d)
for i, dd in enumerate(d):
    x = np.linspace(-14, 14, 4000)
    p = np.exp(-x**2 / (2 * sigma**2))
    q = np.exp(-(x - dd) ** 2 / (2 * sigma**2))
    m = (p + q) / 2

    def kl(a, b):
        mask = a > 1e-12
        return np.trapezoid(a[mask] * np.log(a[mask] / b[mask]), x[mask])

    p /= np.trapezoid(p, x)
    q /= np.trapezoid(q, x)
    m = m / np.trapezoid(m, x)
    js[i] = 0.5 * kl(p, m) + 0.5 * kl(q, m)

fig, axes = plt.subplots(2, 1, figsize=(W_FULL, 3.3),
                         gridspec_kw=dict(height_ratios=[1, 1], hspace=0.55))
ax = axes[0]
ax.plot(d, js, color=BLUE, lw=1.5)
ax.axhline(np.log(2), color=GRAY, lw=0.8, ls=(0, (4, 3)))
ax.text(5.4, np.log(2) - 0.04, "$\\log 2$", fontsize=8.4, color=GRAY)
ax.set_xlabel("两条高斯均值的距离 $|\\mu_1-\\mu_2|$")
ax.set_ylabel("JS 散度")
ax.set_ylim(0, 0.78)
style(ax, spines=("top", "right"))

ax = axes[1]
for dd, c, lab in [(0.5, BLUE, "距离 0.5"), (4.0, RED, "距离 4")]:
    x = np.linspace(-4, 8, 800)
    p = np.exp(-x**2 / 2)
    q = np.exp(-(x - dd) ** 2 / 2)
    D = p / (p + q + 1e-12)
    ax.plot(x, D, color=c, lw=1.3, label=lab)
ax.set_xlabel("$x$")
ax.set_ylabel("$D^*(x)$")
ax.set_ylim(-0.05, 1.08)
ax.legend(loc="center left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig05_js", CH)

# ---------- 图 4.2 模式坍塌 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.82, 2.25))
x = np.linspace(-7, 7, 800)
peaks = [-4.2, 0.0, 4.2]
p_real = sum(np.exp(-(x - c) ** 2 / (2 * 0.75**2)) for c in peaks) / 3
p_gen = np.exp(-(x - 0.0) ** 2 / (2 * 0.75**2))
ax.fill_between(x, p_real, color="#c8c8c5", alpha=0.55, lw=0, label="真实分布")
ax.plot(x, p_real, color=GRAY, lw=1.0)
ax.plot(x, p_gen, color=BLUE, lw=1.5, label="生成分布")
ax.set_yticks([])
ax.set_xlabel("$x$")
ax.legend(loc="upper right", fontsize=8.0)
style(ax, spines=("top", "right"))
ax.annotate("两个峰从未被采样", xy=(-4.2, 0.72), xytext=(-6.7, 0.95), fontsize=8.0,
            color=GRAY, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
save(fig, "fig05_mode", CH)
