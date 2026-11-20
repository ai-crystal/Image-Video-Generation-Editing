import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "10"

# ---------- 图 10.1 瞬时速度与平均速度 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.58, 2.3))
t = np.linspace(0, 1, 300)
x = 1.0 - 1.7 * t + 0.45 * np.sin(np.pi * t)
y = 0.8 - 1.5 * t - 0.25 * np.sin(2 * np.pi * t)
ax.plot(x, y, color=BLUE, lw=1.5)
i0 = 90
tx, ty = np.gradient(x), np.gradient(y)
nrm = np.hypot(tx, ty)
ax.annotate("", xy=(x[i0] + 0.45 * tx[i0] / nrm[i0], y[i0] + 0.45 * ty[i0] / nrm[i0]),
            xytext=(x[i0], y[i0]),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4, mutation_scale=10))
ax.text(x[i0] + 0.5 * tx[i0] / nrm[i0], y[i0] + 0.52 * ty[i0] / nrm[i0], "$v$", color=RED, fontsize=11)
ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[i0], y[i0]),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4, mutation_scale=10))
ax.text(0.5 * (x[i0] + x[-1]) + 0.06, 0.5 * (y[i0] + y[-1]) - 0.12, "$u$", color=GREEN, fontsize=11)
ax.scatter([x[0]], [y[0]], s=28, c="#b9b9b6", zorder=5)
ax.scatter([x[-1]], [y[-1]], s=28, c=BLUE, zorder=5)
ax.text(x[0] + 0.04, y[0] + 0.05, "起点", fontsize=8.0, color=GRAY)
ax.text(x[-1] + 0.05, y[-1] - 0.14, "终点", fontsize=8.0, color=BLUE)
ax.set_xlabel("$z_1$")
ax.set_ylabel("$z_2$")
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig10_geometry", CH)

# ---------- 图 10.2 一步与多步的误差 ----------
mu = np.array([-1.4, 1.4])
sd = 0.5


def field(x, t):
    if t < 1e-4:
        return np.zeros_like(x)
    a, s = 1 - t, t
    d = x[None, :] - a * mu[:, None]
    logw = -0.5 * (d ** 2) / (a ** 2 * sd ** 2 + s ** 2)
    logw -= logw.max(0, keepdims=True)
    w = np.exp(logw)
    w /= w.sum(0, keepdims=True)
    m = (w * mu[:, None]).sum(0)
    return -x + a * m


def integrate(x1, n):
    x = x1.copy()
    dt = -1.0 / n
    for i in range(n):
        t = 1 + i * dt
        x = x + dt * field(x, max(t, 0.0))
    return x


x1 = np.linspace(-2.2, 2.2, 41)
truth = integrate(x1, 4000)

fig, ax = plt.subplots(figsize=(W_FULL * 0.78, 2.15))
ns = [1, 2, 3, 5, 8, 12, 20, 40]
errs = [np.abs(integrate(x1, n) - truth).mean() for n in ns]
ax.loglog(ns, errs, "o-", color=BLUE, ms=3.6, lw=1.3, label="Euler（瞬时速度）")
ax.axhline(errs[-1], color=RED, lw=1.1, ls=(0, (4, 3)), label="平均速度一步")
ax.set_xlabel("积分步数 $N$")
ax.set_ylabel("平均绝对误差")
ax.legend(loc="lower left", fontsize=7.8)
ax.grid(True, which="both", color=LIGHT, lw=0.5, alpha=0.7)
ax.set_axisbelow(True)
style(ax, spines=("top", "right"))
save(fig, "fig10_error", CH)
