import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "09"

# ---------- 图 9.1 条件均值把两条分支压成中间一条曲线 ----------
MU = np.array([-1.3, 1.3])
SD = 0.30
PI = np.array([0.5, 0.5])
t = 0.6
a = 1.0 - t

rng = np.random.default_rng(7)
n = 300
k = rng.choice(2, size=n, p=PI)
x0 = MU[k] + SD * rng.standard_normal(n)
eps = rng.standard_normal(n)
xt = a * x0 + t * eps

grid = np.linspace(-2.5, 2.5, 500)
var = a ** 2 * SD ** 2 + t ** 2
logw = np.log(PI)[:, None] - 0.5 * (grid[None, :] - a * MU[:, None]) ** 2 / var
logw -= logw.max(0, keepdims=True)
w = np.exp(logw)
w /= w.sum(0, keepdims=True)
post_mean = (w * (MU[:, None] + (a * SD ** 2 / var) * (grid[None, :] - a * MU[:, None]))).sum(0)

fig, ax = plt.subplots(figsize=(W_FULL * 0.72, 2.5))
ax.scatter(xt, x0, s=7, c="#c2c2be", lw=0, zorder=2, label="教师样本对")
ax.plot(grid, post_mean, color=BLUE, lw=1.6, zorder=4, label=r"$E[x_0\mid x_t]$")
ax.axhline(0.0, color=LIGHT, lw=0.8, ls=(0, (3, 3)), zorder=1)
ax.scatter([0.0], [0.0], s=26, c=RED, zorder=6)
ax.annotate("均值落在两峰之间", xy=(-0.04, 0.03), xytext=(-2.15, 0.72),
            fontsize=7.6, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.8,
                            shrinkA=4, shrinkB=5))
ax.set_xlabel(r"$x_t$（$t=0.6$）")
ax.set_ylabel(r"$x_0$")
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.35, 2.35)
ax.legend(loc="lower right", fontsize=7.8, handletextpad=0.5, markerscale=2.6,
          borderaxespad=0.2, labelspacing=0.5)
style(ax)
save(fig, "fig09_regress", CH)

# ---------- 图 9.2 score 差把样本推向数据峰 ----------
PI_D = np.array([0.5, 0.5])
MU_D = np.array([-1.3, 1.3])
SD_D = 0.28
PI_S = np.array([0.40, 0.20, 0.40])
MU_S = np.array([-0.85, 0.0, 0.85])
SD_S = 0.45


def _sdvec(mu, sd):
    sd = np.atleast_1d(np.asarray(sd, dtype=float))
    return np.full(mu.size, sd[0]) if sd.size == 1 else sd


def dens(x, pi, mu, sd):
    sd = _sdvec(mu, sd)
    return (pi[:, None] * np.exp(-0.5 * ((x[None, :] - mu[:, None]) / sd[:, None]) ** 2)
            / (np.sqrt(2 * np.pi) * sd[:, None])).sum(0)


def score(x, pi, mu, sd):
    sd = _sdvec(mu, sd)
    comp = pi[:, None] * np.exp(-0.5 * ((x[None, :] - mu[:, None]) / sd[:, None]) ** 2) / sd[:, None]
    w = comp / comp.sum(0, keepdims=True)
    return (w * (-(x[None, :] - mu[:, None]) / sd[:, None] ** 2)).sum(0)


x = np.linspace(-2.4, 2.4, 600)
pd_ = dens(x, PI_D, MU_D, SD_D)
ps_ = dens(x, PI_S, MU_S, SD_S)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(W_FULL * 0.78, 2.75),
                               sharex=True,
                               gridspec_kw=dict(height_ratios=[1.9, 1.0], hspace=0.30))
ax1.fill_between(x, 0, pd_, color=BLUE_L, alpha=0.42, lw=0, label="数据分布 $p_{\\mathrm{data}}$")
ax1.plot(x, ps_, color=RED, lw=1.4, label="学生分布 $p_\\theta$")
ax1.set_ylabel("密度")
ax1.set_yticks([])
ax1.set_ylim(0, 1.30 * max(pd_.max(), ps_.max()))
ax1.legend(loc="upper center", fontsize=7.6, ncol=2, handlelength=1.3,
           columnspacing=1.6, bbox_to_anchor=(0.5, 1.07))
style(ax1, spines=("top", "right", "bottom"))

xs = np.array([-1.55, -1.15, -0.75, -0.35, 0.0, 0.35, 0.75, 1.15, 1.55])
d = score(xs, PI_D, MU_D, SD_D) - score(xs, PI_S, MU_S, SD_S)
scale = 0.30 / np.abs(d).max()
ax2.axhline(0.0, color=LIGHT, lw=0.9, zorder=1)
for xi, di in zip(xs, d):
    if abs(di) * scale < 0.03:
        ax2.scatter([xi], [0.0], s=12, c=GRAY, zorder=3)
        continue
    ax2.annotate("", xy=(xi + di * scale, 0.0), xytext=(xi, 0.0),
                 arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2,
                                 mutation_scale=9, shrinkA=0, shrinkB=1))
ax2.text(-2.35, 0.135, "$s_{\\mathrm{data}}-s_\\theta$（放大约 12 倍）", fontsize=7.4, color=GREEN)
ax2.set_ylim(-0.16, 0.24)
ax2.set_yticks([])
ax2.set_xlabel("样本位置 $x$")
ax2.set_xlim(-2.4, 2.4)
style(ax2, spines=("top", "right", "left"))
save(fig, "fig09_score", CH)
