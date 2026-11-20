import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "10"
CH9 = "09"
CH10 = "10"

# ---------- 图 10.1 不同引导强度下的采样 ----------
# 两类数据，每类两个峰
class_means = {
    0: np.array([[-1.2, 0.9], [-1.1, -0.9]]),
    1: np.array([[1.2, 0.9], [1.2, -0.9]]),
}
sd = 0.28
prior = {c: 0.5 for c in class_means}


def gauss_score(x, m, s):
    return -(x - m) / (s ** 2)


def cond_score(x, c):
    means = class_means[c]
    logw = []
    for m in means:
        d = x - m
        logw.append(-0.5 * (d ** 2).sum(-1) / sd ** 2)
    logw = np.stack(logw, 1)
    w = np.exp(logw - logw.max(1, keepdims=True))
    w /= w.sum(1, keepdims=True)
    out = 0.0
    for k, m in enumerate(means):
        out = out + w[:, k:k + 1] * gauss_score(x, m, sd)
    return out


def uncond_score(x):
    return 0.5 * cond_score(x, 0) + 0.5 * cond_score(x, 1)


rng = np.random.default_rng(3)
fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.9), gridspec_kw=dict(wspace=0.12))
for ax, w in zip(axes, [1.0, 5.0, 10.0]):
    x = rng.normal(0, 1.4, (240, 2))
    n = 120
    dt = -1.0 / n
    for i in range(n):
        gu = uncond_score(x)
        gc = cond_score(x, 1)
        v = gu + w * (gc - gu)
        x = x + dt * (0.35 * x + 0.65 * v / 4)
    ax.scatter(class_means[0][:, 0], class_means[0][:, 1], s=26, c="#bdbdb9", marker="*")
    ax.scatter(class_means[1][:, 0], class_means[1][:, 1], s=26, c=BLUE, marker="*")
    ax.scatter(x[:, 0], x[:, 1], s=1.6, c=RED, alpha=0.5, lw=0)
    ax.set_title("$w = %g$" % w, fontsize=8.6)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig10_cfg", CH9)

