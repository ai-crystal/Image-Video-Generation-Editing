import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from scipy.stats import norm

CH = "05"

# ---------- 上：一维两条高斯的累积分布，两线之间的面积就是 W1 ----------
d = 2.0
x = np.linspace(-5, 7, 900)
Fp = norm.cdf(x, 0.0, 1.0)
Fq = norm.cdf(x, d, 1.0)

fig, axes = plt.subplots(2, 1, figsize=(W_FULL, 3.35),
                         gridspec_kw=dict(height_ratios=[1, 1], hspace=0.62))

ax = axes[0]
ax.fill_between(x, Fp, Fq, color="#c8c8c5", alpha=0.75, lw=0, label="两线之间的面积")
ax.plot(x, Fp, color=BLUE, lw=1.5, label="$F_{\\mathrm{data}}$")
ax.plot(x, Fq, color=RED, lw=1.5, label="$F_g$")
# 在 u = 0.5 的横线上标出搬运距离
u = 0.5
x1, x2 = norm.ppf(u, 0.0, 1.0), norm.ppf(u, d, 1.0)
ax.plot([x1, x2], [u, u], color=INK, lw=0.8, ls=(0, (2, 2)))
ax.annotate("", xy=(x2, u), xytext=(x1, u),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
ax.text((x1 + x2) / 2, u + 0.07, "距离 %.1f" % d, ha="center", fontsize=8.0, color=INK)
ax.set_xlim(-5, 7)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("$x$")
ax.set_ylabel("累积分布")
ax.legend(loc="upper left", fontsize=8.0)
style(ax)

# ---------- 下：同一组分布，JS 饱和而 W1 线性增长 ----------
dd = np.linspace(0, 6, 240)
js = np.zeros_like(dd)
for i, v in enumerate(dd):
    xx = np.linspace(-18, 18 + v, 12000)
    p = norm.pdf(xx, 0.0, 1.0)
    q = norm.pdf(xx, v, 1.0)
    m = (p + q) / 2
    js[i] = 0.5 * np.trapezoid(p * np.log(p / m), xx) + 0.5 * np.trapezoid(q * np.log(q / m), xx)
xg = np.linspace(-30, 38, 200000)
w1 = np.array([np.trapezoid(np.abs(norm.cdf(xg, 0.0, 1.0) - norm.cdf(xg, v, 1.0)), xg)
               for v in dd])

ax = axes[1]
ax.plot(dd, js, color=BLUE, lw=1.5, label="JS（左轴）")
ax.axhline(np.log(2), color=BLUE_L, lw=0.8, ls=(0, (4, 3)))
ax.text(0.12, np.log(2) + 0.02, "$\\log 2$", color=BLUE, fontsize=8.2)
ax.set_xlabel("两条高斯均值的距离")
ax.set_ylabel("JS", color=BLUE)
ax.set_ylim(0, 0.78)

ax2 = ax.twinx()
ax2.plot(dd, w1, color=RED, lw=1.5, label="$W_1$（右轴）")
ax2.set_ylabel("$W_1$", color=RED)
ax2.set_ylim(0, 8.6)
ax2.spines["top"].set_visible(False)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=8.0)
style(ax)
save(fig, "fig05_w1", CH)
