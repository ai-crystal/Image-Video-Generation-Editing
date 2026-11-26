import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "04"

T = 0.45
MUS = np.array([[-1.15, -0.35], [1.05, -0.25], [0.10, 1.15]])
VAR0 = 0.075


def mixture(x, t):
    """线性路径下 p_t 的密度与分数，数据为三个各向同性高斯"""
    x = np.atleast_2d(np.asarray(x, dtype=float))
    m = (1 - t) * MUS
    s2 = (1 - t) ** 2 * VAR0 + t ** 2
    logw = -((x[:, None, :] - m[None, :, :]) ** 2).sum(-1) / (2 * s2)
    logw -= logw.max(1, keepdims=True)
    w = np.exp(logw)
    w = w / w.sum(1, keepdims=True)
    k = MUS.shape[0]
    logp = -np.log(k) - np.log(2 * np.pi * s2) - 0.5 * (
        (x[:, None, :] - m[None, :, :]) ** 2).sum(-1) / s2
    mx = logp.max(1, keepdims=True)
    dens = np.exp(mx[:, 0]) * np.exp(logp - mx).sum(1)
    score = ((-(x[:, None, :] - m[None, :, :]) / s2) * w[:, :, None]).sum(1)
    return dens, score


def velocity(x, t):
    _, sc = mixture(x, t)
    return -(np.asarray(x, dtype=float) + t * sc) / (1 - t)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.5), gridspec_kw=dict(wspace=0.3))

# ---------- 左：速度场 ----------
ax = axes[0]
gg = np.linspace(-2.3, 2.3, 220)
GX, GY = np.meshgrid(gg, gg)
D, _ = mixture(np.stack([GX.ravel(), GY.ravel()], 1), T)
ax.contour(GX, GY, np.log(D).reshape(GX.shape), levels=8, colors=["#b7b7b2"], linewidths=0.65)

q = np.linspace(-2.0, 2.0, 12)
QX, QY = np.meshgrid(q, q)
V = velocity(np.stack([QX.ravel(), QY.ravel()], 1), T)
VX = V[:, 0].reshape(QX.shape)
VY = V[:, 1].reshape(QX.shape)
norm = np.sqrt(VX ** 2 + VY ** 2) + 1e-9
ax.quiver(QX, QY, VX / norm * 0.34, VY / norm * 0.34, color=BLUE, angles="xy",
          scale_units="xy", scale=1, width=0.0032, headwidth=4, headlength=4.5)
ax.set_xlabel("$x^{(1)}$")
ax.set_ylabel("$x^{(2)}$")
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-2.3, 2.3)
ax.set_aspect("equal")
style(ax)

# ---------- 右：一个点上的两项分解 ----------
ax = axes[1]
gg = np.linspace(-2.0, 2.0, 160)
GX, GY = np.meshgrid(gg, gg)
D, _ = mixture(np.stack([GX.ravel(), GY.ravel()], 1), T)
ax.contour(GX, GY, np.log(D).reshape(GX.shape), levels=8, colors=["#d2d2ce"], linewidths=0.6)

xs = np.array([-0.55, -0.55])
_, sc = mixture(xs, T)
sc = np.asarray(sc).reshape(-1, 2)[0]
a = -xs / (1 - T)
b = -T / (1 - T) * sc
v = a + b

arr = dict(arrowstyle="-|>", mutation_scale=9, shrinkA=0, shrinkB=0)
ax.annotate("", xy=xs + a, xytext=xs, arrowprops=dict(color=GRAY, lw=1.3, **arr))
ax.annotate("", xy=xs + a + b, xytext=xs + a, arrowprops=dict(color=SAND, lw=1.3, **arr))
ax.annotate("", xy=xs + v, xytext=xs, arrowprops=dict(color=RED, lw=1.7, **arr))
ax.scatter([xs[0]], [xs[1]], s=15, c=INK, zorder=6)
ax.text(xs[0] - 0.09, xs[1] + 0.12, "$x_t$", fontsize=9, color=INK)
ax.text(xs[0] - 0.05, xs[1] + 1.16, r"$-\frac{x_t}{1-t}$", color=GRAY, fontsize=9)
ax.text(xs[0] + 1.12, xs[1] - 0.22, r"$-\frac{t}{1-t}\nabla\log p_t$", color=SAND, fontsize=9)
ax.text(xs[0] + 0.30, xs[1] - 0.36, "$v$", color=RED, fontsize=9.5)
ax.set_xlabel("$x^{(1)}$")
ax.set_ylabel("$x^{(2)}$")
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_aspect("equal")
style(ax)
save(fig, "fig04_decomp", CH)
