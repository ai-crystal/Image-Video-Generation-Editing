import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "06"

mu = np.array([[-1.1, 0.5], [1.1, 0.6], [0.0, -0.95]])
cov = np.tile(np.eye(2) * 0.06, (3, 1, 1))


def score_fn(x, t):
    ab = np.exp(-3.0 * t)
    s2 = 1 - ab
    ws = []
    for k in range(3):
        C = ab * cov[k] + s2 * np.eye(2)
        Ci = np.linalg.inv(C)
        d = x - np.sqrt(ab) * mu[k]
        ws.append(-0.5 * d @ Ci @ d - 0.5 * np.log(np.linalg.det(C)))
    ws = np.array(ws)
    ws = np.exp(ws - ws.max())
    ws /= ws.sum()
    out = np.zeros(2)
    for k in range(3):
        C = ab * cov[k] + s2 * np.eye(2)
        out += ws[k] * (-np.linalg.solve(C, x - np.sqrt(ab) * mu[k]))
    return out


fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.95), gridspec_kw=dict(wspace=0.12))
rng = np.random.default_rng(21)
for ax, eps in zip(axes, [0.0, 0.35, 1.2]):
    x = rng.normal(0, 0.9, (5, 2))
    n = 240
    dt = -1.0 / n
    path = np.zeros((n + 1, len(x), 2))
    path[0] = x
    for i in range(n):
        t = 1 + i * dt
        for j in range(len(x)):
            s = score_fn(path[i, j], t)
            drift = -0.5 * 3.0 * path[i, j] - 0.5 * 3.0 * s + 0.5 * eps * s
            noise = np.sqrt(eps * abs(dt)) * rng.normal(0, 1, 2)
            path[i + 1, j] = path[i, j] + dt * drift + noise
    for j in range(len(x)):
        ax.plot(path[:, j, 0], path[:, j, 1], color=BLUE_L, lw=0.6, alpha=0.85)
    ax.scatter(mu[:, 0], mu[:, 1], s=22, c=BLUE, marker="*", zorder=4)
    ax.text(0.5, 0.94, "$\\epsilon_t=%.2f$" % eps, transform=ax.transAxes,
            ha="center", fontsize=8.2, color=GRAY)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.2, 2.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig06_sde", CH)
