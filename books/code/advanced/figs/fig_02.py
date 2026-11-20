import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "02"

# ---------- 图 2.1 连续流把高斯搬到环状分布 ----------
K = 9
phi = np.linspace(0, 2 * np.pi, K, endpoint=False)
mu = np.stack([1.05 * np.cos(phi), 0.62 * np.sin(phi)], 1)
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


rng = np.random.default_rng(11)
starts = rng.normal(0, 1.0, (48, 2))
n = 320
dt = -1.0 / n
traj = np.zeros((n + 1, len(starts), 2))
traj[0] = starts
for i in range(n):
    t = 1 + i * dt
    for j in range(len(starts)):
        traj[i + 1, j] = traj[i, j] + dt * field(traj[i, j], max(t, 0.0))

fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.45))
for j in range(len(starts)):
    ax.plot(traj[:, j, 0], traj[:, j, 1], color=BLUE_L, lw=0.5, alpha=0.55)
ax.scatter(traj[-1, :, 0], traj[-1, :, 1], s=3.2, c=BLUE, alpha=0.9, lw=0)
ax.scatter(traj[0, :, 0], traj[0, :, 1], s=3.2, c="#b9b9b6", alpha=0.9, lw=0)
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.text(-2.2, 1.28, "起点：标准高斯", fontsize=8.2, color=GRAY)
ax.text(1.0, -1.42, "终点：数据分布", fontsize=8.2, color=BLUE)
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig02_flow", CH)

# ---------- 图 3.1 两种路径 ----------
CH = "03"
t = np.linspace(0, 1, 300)
fig, ax = plt.subplots(figsize=(W_FULL * 0.62, 2.25))
ax.plot(1 - t, t, color=BLUE, lw=1.5, label="直线路径")
ax.plot(np.cos(t * np.pi / 2), np.sin(t * np.pi / 2), color=RED, lw=1.5, label="VP 路径")
ax.scatter([1], [0], s=26, c=INK, zorder=5)
ax.scatter([0], [1], s=26, c=INK, zorder=5)
ax.text(1.04, -0.09, "数据", fontsize=8.2)
ax.text(-0.06, 1.06, "噪声", fontsize=8.2)
ax.set_xlabel("$\\alpha_t$")
ax.set_ylabel("$\\sigma_t$")
ax.set_xlim(-0.05, 1.2)
ax.set_ylim(-0.05, 1.15)
ax.set_aspect("equal")
ax.legend(loc="center right", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig03_alpha", CH)
