import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "18"

# 两个标准差 0.1 的高斯，均值 ±1。线性插值路径下的条件均值 m(x,t) = E[x_0 | x_t = x]。
S = 0.1


def post_mean(x, t):
    vt = (1 - t) ** 2 * S ** 2 + t ** 2
    return (1 - t) * np.tanh(2 * (1 - t) * x / vt)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.4), gridspec_kw=dict(wspace=0.32))

# 左：一步映射的形状随起点变化。x_0 = z - t * u(z,t) 在该路径上恰好等于 m(z,t)。
ax = axes[0]
grid = np.linspace(-3, 3, 600)
for t, c in [(1.0, GRAY), (0.6, BLUE), (0.3, RED)]:
    ax.plot(grid, post_mean(grid, t), color=c, lw=1.4, label="$t_{\\mathrm{start}}=%.1f$" % t)
ax.axhline(0, color=LIGHT, lw=0.8, zorder=0)
ax.set_xlabel("输入噪声 $z$")
ax.set_ylabel("一步输出 $x_0$")
ax.set_xlim(-3, 3)
ax.set_ylim(-1.15, 1.15)
ax.legend(loc="lower right", handlelength=1.4)
style(ax, grid=True)

# 右：同一个映射作用在 z ~ N(0,1) 上得到的输出分布
ax = axes[1]
rng = np.random.default_rng(3)
z = rng.normal(size=200000)
levels = [(1.0, GRAY), (0.8, BLUE_L), (0.6, BLUE), (0.4, SAND), (0.2, RED)]
bins = np.linspace(-1.4, 1.4, 121)
for i, (t, c) in enumerate(levels):
    out = post_mean(z, t)
    h, e = np.histogram(out, bins=bins, density=True)
    xc = 0.5 * (e[1:] + e[:-1])
    h = np.convolve(h, np.ones(3) / 3, mode="same")
    h = h / h.max()
    base = -i * 1.05
    ax.fill_between(xc, base, base + h, color=c, alpha=0.28, lw=0)
    ax.plot(xc, base + h, color=c, lw=1.1)
    ax.text(-1.36, base + 0.18, "$t=%.1f$" % t, fontsize=8, color=c)
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-5.1, 1.5)
ax.set_yticks([])
ax.set_xlabel("一步输出的 $x_0$")
ax.set_ylabel("输出分布")
style(ax, grid=False)

save(fig, "fig18_posterior", CH)
