import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "22"

# ---------- 图 22.1 ControlNet 结构 ----------
fig, ax = plt.subplots(figsize=(W_FULL, 2.45))
ax.set_xlim(0, 11.95)
ax.set_ylim(0, 6.1)
ax.axis("off")


def box(x, y, w, h, label, fc="#eef2f6", ec=BLUE, ls="-", fs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9, ls=ls))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK)


def arr(x0, y0, x1, y1, c=GRAY, lw=0.9, rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                connectionstyle="arc3,rad=%s" % rad))


box(2.9, 4.0, 2.0, 1.0, "冻结编码器", fc="#f4f4f2", ls=(0, (3, 2)))
box(2.9, 1.6, 2.0, 1.0, "可训练副本", fc="#e8eff6")
box(1.9, 0.3, 2.0, 0.8, "hint 卷积", fs=6.9)
box(5.1, 1.6, 1.2, 1.0, "零卷积", fc="#fdf3e3", ec=SAND, fs=6.9)
box(7.0, 3.5, 1.0, 1.6, "相加", fc="#ffffff", ec=GRAY)
box(8.5, 3.55, 1.8, 1.5, "冻结解码器", fc="#f4f4f2", ls=(0, (3, 2)), fs=6.9)

ax.text(0.3, 4.62, "$z_t$", fontsize=8.4, color=INK)
ax.plot([0.62, 2.45], [4.5, 4.5], color=GRAY, lw=0.9)
ax.plot([2.45, 2.45], [4.5, 2.1], color=GRAY, lw=0.9)
arr(2.45, 4.5, 2.85, 4.5)
arr(2.45, 2.1, 2.85, 2.1)

ax.text(1.05, 0.80, "条件图 $c_f$", fontsize=7.2, color=GRAY, ha="center", va="bottom")
arr(0.22, 0.72, 1.85, 0.72)
arr(3.6, 1.14, 3.6, 1.55)

arr(4.95, 2.1, 5.05, 2.1)
arr(4.95, 4.5, 6.95, 4.5)
ax.plot([6.35, 7.5], [2.1, 2.1], color=SAND, lw=0.9)
arr(7.5, 2.1, 7.5, 3.45, c=SAND)
arr(8.05, 4.3, 8.45, 4.3)
arr(10.35, 4.3, 10.85, 4.3)

ax.text(11.9, 4.3, "输出", fontsize=7.2, color=GRAY, ha="right")
ax.text(5.7, 1.26, "零初始化", fontsize=6.9, color=SAND, ha="center")
save(fig, "fig22_controlnet", CH)

# ---------- 图 22.2 反演漂移 ----------
t = np.linspace(0, 1, 300)
true = 0.92 * np.cos(2.1 * t) + 0.08
inv = true + 0.17 * t ** 2.1
fig, ax = plt.subplots(figsize=(W_FULL * 0.76, 2.1))
ax.plot(t, true, color=RED, lw=1.5, label="真实前向轨迹")
ax.plot(t, inv, color=BLUE, lw=1.5, label="反演轨迹")
ax.fill_between(t, true, inv, color=BLUE, alpha=0.12, lw=0)
ax.set_xlabel("$t$")
ax.set_ylabel("$x_t$（某一维）")
ax.set_yticks([])
ax.legend(loc="lower left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig22_drift", CH)

# ---------- 图 22.3 一阶与二阶反演的误差 ----------
T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)
sq = np.sqrt(abar)
mu = np.array([-1.2, 1.2])
sd = np.array([0.35, 0.45])
w = np.array([0.5, 0.5])


def eps(x, i):
    x = np.asarray(x, float)
    a, s = abar[i], sq[i]
    v = a * sd ** 2 + (1 - a)
    m = s * mu
    xb = x[None, ...]
    lp = (-0.5 * (xb - m[:, None]) ** 2 / v[:, None]
          - 0.5 * np.log(2 * np.pi * v[:, None]) + np.log(w)[:, None])
    lp -= lp.max(axis=0, keepdims=True)
    p = np.exp(lp)
    p /= p.sum(axis=0, keepdims=True)
    return -np.sqrt(1 - a) * np.sum(p * (-(xb - m[:, None]) / v[:, None]), axis=0)


def step(x, i, j, e):
    x0 = (x - np.sqrt(1 - abar[i]) * e) / sq[i]
    return sq[j] * x0 + np.sqrt(1 - abar[j]) * e


def down(x, i, j):
    return step(x, i, j, eps(x, i))


def up1(x, i, j):
    return step(x, i, j, eps(x, i))


def up2(x, i, j):
    xa = up1(x, i, j)
    return step(x, i, j, 0.5 * (eps(x, i) + eps(xa, j)))


def up3(x, i, j):
    xa = up1(x, i, j)
    return step(x, i, j, eps(xa, j))


rng = np.random.default_rng(0)
xT0 = rng.normal(0, 1, 64)
Ns = np.array([10, 20, 50, 100, 200, 500])
res = {k: [] for k in ("一阶", "双向平均", "不动点")}
for N in Ns:
    idx = np.linspace(T - 1, 0, N + 1).astype(int)
    x = xT0.copy()
    for k in range(N):
        x = down(x, idx[k], idx[k + 1])
    x0 = x.copy()
    for name, fn in (("一阶", up1), ("双向平均", up2), ("不动点", up3)):
        xi = x0.copy()
        for k in range(N - 1, -1, -1):
            xi = fn(xi, idx[k + 1], idx[k])
        res[name].append(np.sqrt(np.mean((xi - xT0) ** 2)))

fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.35))
for name, c in (("一阶", BLUE), ("双向平均", SAND), ("不动点", GREEN)):
    ax.loglog(Ns, res[name], "o-", ms=3.2, lw=1.3, color=c, label=name)
ref = res["一阶"][0] * (Ns / Ns[0]) ** -1.0
ax.loglog(Ns, ref, "--", color=GRAY, lw=0.9)
ax.text(330, 0.0016, "虚线斜率 $-1$", fontsize=7.4, color=GRAY, ha="center")
ax.set_xlabel("反演步数 $N$")
ax.set_ylabel("回到 $x_T$ 的 RMS 误差")
ax.legend(loc="lower left", fontsize=7.6)
style(ax, grid=True, spines=("top", "right"))
save(fig, "fig22_order", CH)

for name in res:
    print(name, [round(v, 5) for v in res[name]])
