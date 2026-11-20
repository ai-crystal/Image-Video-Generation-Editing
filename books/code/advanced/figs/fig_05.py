import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "05"

# ---------- 图 5.1 一维交叉 ----------
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.2), gridspec_kw=dict(wspace=0.3))
ax = axes[0]
for x0, x1 in [(-1, -0.9), (-1, 0.9), (1, -0.9), (1, 0.9)]:
    ax.plot([x1, x0], [1, 0], color=BLUE_L, lw=1.0)
    ax.scatter([x1], [1], s=16, c="#b9b9b6", zorder=4)
    ax.scatter([x0], [0], s=16, c=BLUE, zorder=4)
ax.set_xlabel("$x$")
ax.set_ylabel("$t$")
ax.set_yticks([0, 1])
ax.set_yticklabels(["0", "1"])
ax.set_ylim(-0.15, 1.15)
ax.set_xlim(-1.6, 1.6)
style(ax, spines=("top", "right"))

ax = axes[1]
tt = np.linspace(0, 1, 300)
xx = 0.95 - 1.9 * tt + 0.55 * np.sin(np.pi * tt)
ax.plot(xx, tt, color=RED, lw=1.5)
for i in range(0, len(tt), 40):
    ax.annotate("", xy=(xx[i] + 0.02, tt[i] + 0.03), xytext=(xx[i], tt[i]),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9, mutation_scale=7))
ax.set_xlabel("$x$")
ax.set_yticks([0, 1])
ax.set_yticklabels(["0", "1"])
ax.set_ylim(-0.15, 1.15)
ax.set_xlim(-1.6, 1.6)
style(ax, spines=("top", "right"))
save(fig, "fig05_bend", CH)

# ---------- 图 5.2 重配对前后 ----------
K = 9
phi = np.linspace(0, 2 * np.pi, K, endpoint=False)
mu = np.stack([1.05 * np.cos(phi), 0.6 * np.sin(phi)], 1)
sd = 0.1


def field(x, t):
    if t < 1e-3:
        return np.zeros_like(x)
    a, s = 1 - t, t
    d = x[None, :] - a * mu
    logw = -0.5 * (d ** 2).sum(1) / (a ** 2 * sd ** 2 + s ** 2 + 1e-9)
    logw -= logw.max()
    w = np.exp(logw)
    w /= w.sum()
    m = (w[:, None] * mu).sum(0)
    return -x + a * m


rng = np.random.default_rng(12)
starts = rng.normal(0, 1.0, (26, 2))
n = 260
dt = -1.0 / n
traj = np.zeros((n + 1, len(starts), 2))
traj[0] = starts
for i in range(n):
    t = 1 + i * dt
    for j in range(len(starts)):
        traj[i + 1, j] = traj[i, j] + dt * field(traj[i, j], max(t, 0.0))

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.22))
ax = axes[0]
for j in range(len(starts)):
    ax.plot(traj[:, j, 0], traj[:, j, 1], color=BLUE_L, lw=0.55, alpha=0.85)
ax.scatter(traj[-1, :, 0], traj[-1, :, 1], s=4.2, c=BLUE, zorder=4)
ax = axes[1]
for j in range(len(starts)):
    ax.plot([starts[j, 0], traj[-1, j, 0]], [starts[j, 1], traj[-1, j, 1]],
            color=BLUE_L, lw=0.55, alpha=0.85)
ax.scatter(traj[-1, :, 0], traj[-1, :, 1], s=4.2, c=BLUE, zorder=4)
for ax in axes:
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.7, 1.7)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig05_reflow", CH)
