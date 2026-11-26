import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "03"

# ---------- 图 3.2 时间标签与信噪比 ----------
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3), gridspec_kw=dict(wspace=0.34))

ax = axes[0]
t = np.linspace(0, 1, 400)
ax.plot(1 - t, t, color=BLUE, lw=1.6, zorder=2)
n = np.array([1.0, 1.0]) / np.sqrt(2)
for tt in np.linspace(0, 1, 11):
    p = np.array([1 - tt, tt])
    ax.plot(*np.stack([p - 0.05 * n, p + 0.05 * n]).T, color=BLUE, lw=1.0, zorder=3)
for tt in np.linspace(0, 1, 6):
    s = tt ** 2
    p = np.array([1 - s, s])
    ax.plot(*np.stack([p - 0.09 * n, p + 0.09 * n]).T, color=RED, lw=1.3, zorder=4)
ax.text(0.50, 0.87, "$t$：等间隔", color=BLUE, transform=ax.transAxes, fontsize=8.6)
ax.text(0.30, 0.06, "$s=t^2$：密度不均", color=RED, transform=ax.transAxes, fontsize=8.6)
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel(r"$\sigma$")
ax.set_xlim(-0.05, 1.08)
ax.set_ylim(-0.05, 1.08)
style(ax)

ax = axes[1]
tt = np.linspace(0.006, 0.994, 400)
ax.plot(tt, 2 * np.log((1 - tt) / tt), color=BLUE, lw=1.5, label="直线")
ax.plot(tt, 2 * np.log(np.cos(np.pi * tt / 2) / np.sin(np.pi * tt / 2)), color=GREEN, lw=1.5, label="VP")
for k in range(1, 10):
    ax.plot([k / 10], [2 * np.log((1 - k / 10) / (k / 10))], "|", color=BLUE, ms=5, mew=1.0)
ax.axhline(0, color=GRAY, lw=0.7, ls=":")
ax.set_xlabel("$t$")
ax.set_ylabel(r"$\log(\alpha_t^2/\sigma_t^2)$")
ax.set_ylim(-8, 8)
ax.set_xlim(0, 1)
ax.legend(loc="upper right", handlelength=1.5)
style(ax)
save(fig, "fig03_sched", CH)


# ---------- 图 3.3 条件直线很直，边际场会弯 ----------
modes = np.array([[1.35, 0.35], [-1.05, 0.95], [-0.45, -1.25], [0.75, -0.95]])
COL = [BLUE, RED, GREEN, SAND]


def e0(x, t):
    """四峰数据的后验期望 E[x0 | x_t = x]（精确计算）"""
    x = np.asarray(x, dtype=float)
    diff = x[None, :] - (1 - t) * modes
    w = np.exp(-(diff ** 2).sum(1) / (2 * t ** 2))
    w = w / w.sum()
    return w @ modes


def vel(x, t):
    m = e0(x, t)
    return -m + (np.asarray(x, dtype=float) - (1 - t) * m) / t


rng = np.random.default_rng(3)
xn = rng.normal(size=(160, 2))

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.55), gridspec_kw=dict(wspace=0.3))

ax = axes[0]
for i in range(0, 160, 20):
    for k in range(4):
        ax.plot([xn[i, 0], modes[k, 0]], [xn[i, 1], modes[k, 1]],
                color=COL[k], lw=0.55, alpha=0.55)
ax.scatter(xn[:, 0], xn[:, 1], s=3.0, c="#a8a8a5", zorder=3)
for k in range(4):
    ax.scatter([modes[k, 0]], [modes[k, 1]], s=16, c=COL[k], zorder=4)
ax.set_xlabel("$x^{(1)}$")
ax.set_ylabel("$x^{(2)}$")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
style(ax)

ax = axes[1]
g = np.linspace(-2.6, 2.6, 21)
GX, GY = np.meshgrid(g, g)
VX = np.zeros_like(GX)
VY = np.zeros_like(GX)
for i in range(GX.shape[0]):
    for j in range(GX.shape[1]):
        vv = vel([GX[i, j], GY[i, j]], 0.3)
        VX[i, j], VY[i, j] = vv
ax.streamplot(GX, GY, VX, VY, color="#9a9a97", linewidth=0.6, density=1.15,
              arrowsize=0.55, zorder=1)
for k, start in enumerate([5, 47, 91, 133]):
    x = xn[start].copy()
    xs = [x.copy()]
    for s in np.linspace(1, 0.02, 400):
        x = x - 0.01 * vel(x, s)
        xs.append(x.copy())
    xs = np.array(xs)
    ax.plot(xs[:, 0], xs[:, 1], color=COL[k], lw=1.3, zorder=5)
    ax.scatter([xs[0, 0]], [xs[0, 1]], s=10, c="#a8a8a5", zorder=6)
for k in range(4):
    ax.scatter([modes[k, 0]], [modes[k, 1]], s=16, c=COL[k], zorder=7)
ax.set_xlabel("$x^{(1)}$")
ax.set_ylabel("$x^{(2)}$")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
style(ax)
save(fig, "fig03_avg", CH)
