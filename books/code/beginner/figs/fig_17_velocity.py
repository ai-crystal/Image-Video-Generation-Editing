import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "17"

# 数据：两个标准差 S 的高斯，均值 ±1。线性插值路径 x_t = (1-t) x_0 + t x_1 的边缘速度为
# u(x,t) = (x - E[x_0|x_t=x]) / t。
S = 0.1


def post_mean(x, t):
    v = (1 - t) ** 2 * S * S + t * t
    mp, mm = 1 - t, -(1 - t)
    cov = (1 - t) * S * S
    lp = -(x - mp) ** 2 / (2 * v)
    lm = -(x - mm) ** 2 / (2 * v)
    top = max(lp, lm)
    a, b = np.exp(lp - top), np.exp(lm - top)
    ep = 1 + cov * (x - mp) / v
    em = -1 + cov * (x - mm) / v
    return (a * ep + b * em) / (a + b)


def vel(x, t):
    if t < 1e-9:
        return 0.0
    return (x - post_mean(x, t)) / t


def integrate(x0, n, t_end=1e-6):
    ts = np.linspace(1.0, t_end, n + 1)
    x = x0
    xs = [x]
    for i in range(n):
        t, h = ts[i], ts[i + 1] - ts[i]
        k1 = vel(x, t)
        k2 = vel(x + h / 2 * k1, t + h / 2)
        k3 = vel(x + h / 2 * k2, t + h / 2)
        k4 = vel(x + h * k3, t + h)
        x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xs.append(x)
    return np.array(xs), ts


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.35), gridspec_kw=dict(wspace=0.3))

ax = axes[0]
grid = np.linspace(-2.6, 2.6, 800)
for t, c, lab in [(1.0, GRAY, "$t=1.0$"), (0.5, BLUE, "$t=0.5$"), (0.2, RED, "$t=0.2$")]:
    ax.plot(grid, [vel(x, t) for x in grid], color=c, lw=1.4, label=lab)
ax.axhline(0, color=LIGHT, lw=0.8, zorder=0)
ax.axvline(0, color=LIGHT, lw=0.8, zorder=0)
ax.set_xlabel("$x$")
ax.set_ylabel("$u(x,t)$")
ax.set_ylim(-2.2, 2.2)
ax.legend(loc="lower right", handlelength=1.4)
style(ax, grid=False)

ax = axes[1]
for z, c in [(0.45, BLUE_L), (1.5, BLUE), (2.6, RED)]:
    xs, ts = integrate(z, 4000)
    ax.plot(ts, xs, color=c, lw=1.4)
    print(round(z, 2), np.round([xs[int(f * 4000)] for f in (0, 0.25, 0.5, 0.75, 1)], 3))
ax.plot([1, 0], [1.5, 1.11], color=LIGHT, lw=0.9, ls="--")
ax.set_xlim(1.02, -0.02)
ax.set_ylim(-0.1, 2.75)
ax.set_xlabel("$t$（采样从左向右）")
ax.set_ylabel("$x_t$")
style(ax, grid=True)

save(fig, "fig17_velocity", CH)
