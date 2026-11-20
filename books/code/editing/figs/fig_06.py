import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 6.1 受控 ODE ----------
CH = "06"
fig, ax = plt.subplots(figsize=(W_FULL * 0.7, 2.25))
t = np.linspace(0, 1, 200)
base = np.stack([0.9 - 1.4 * t + 0.35 * np.sin(np.pi * t), 0.7 - 1.1 * t], 1)
ctrl = np.stack([0.9 - 0.9 * t, 0.7 - 0.7 * t], 1)
ax.plot(base[:, 0], base[:, 1], color=BLUE, lw=1.5, label="$\\gamma=0$：精确重建")
ax.plot(ctrl[:, 0], ctrl[:, 1], color=RED, lw=1.5, label="$\\gamma=1$：终点典型")
mid = 0.5 * (base + ctrl)
ax.plot(mid[:, 0], mid[:, 1], color=SAND, lw=1.2, ls=(0, (4, 3)), label="中间 $\\gamma$")
ax.scatter([0.9], [0.7], s=26, c=INK, zorder=5)
ax.scatter([-0.5, -0.0], [-0.4, 0.0], s=26, c="#9a9a9a", zorder=5)
ax.set_xlabel("$z_1$")
ax.set_ylabel("$z_2$")
ax.legend(loc="upper left", fontsize=7.4)
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right"))
save(fig, "fig06_rf", CH)

# ---------- 图 7.1 噪声水平 ----------
CH = "07"
fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.0))
tt = np.linspace(0, 1, 200)
ax.plot(tt, np.minimum(1, 2 * tt), color=BLUE, lw=1.5, label="先反演再生成")
ax.plot(tt, 0.05 * np.ones_like(tt), color=RED, lw=1.5, label="直接路径（免反演）")
ax.set_xlabel("过程进度")
ax.set_ylabel("噪声水平")
ax.set_ylim(0, 1.1)
ax.legend(loc="center right", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig07_fe", CH)

# ---------- 图 8.1 drift 与平滑 ----------
CH = "08"
rng = np.random.default_rng(7)
xs = np.linspace(0, 6, 26)
raw = 0.55 * np.sin(2.4 * xs) + 0.35 * rng.normal(0, 1, len(xs)) + 0.9
smooth = np.convolve(raw, np.ones(5) / 5, mode="same")
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 1.95), gridspec_kw=dict(wspace=0.3))
for ax, y, c in [(axes[0], raw, RED), (axes[1], smooth, BLUE)]:
    for xi, yi in zip(xs, y):
        ax.annotate("", xy=(xi, yi), xytext=(xi, 0.15),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=0.8, mutation_scale=6))
    ax.axhline(0.15, color=LIGHT, lw=0.6)
    ax.set_xlim(-0.2, 6.2)
    ax.set_ylim(0, 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig08_drift", CH)

# ---------- 图 8.2 权重 ----------
t = np.linspace(0.05, 1.0, 300)
fig, ax = plt.subplots(figsize=(W_FULL * 0.76, 2.0))
for dl, c in [(0.05, BLUE), (0.15, SAND), (0.35, RED)]:
    ax.plot(t, t / (t + dl), color=c, lw=1.3, label="$\\delta=%g$" % dl)
ax.set_xlabel("$t$")
ax.set_ylabel("上一时刻观测的权重")
ax.set_ylim(0.4, 1.0)
ax.legend(fontsize=8.0, loc="lower right")
style(ax, spines=("top", "right"))
save(fig, "fig08_weight", CH)
