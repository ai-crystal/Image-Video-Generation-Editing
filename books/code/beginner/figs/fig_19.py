import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ---------- 图 13.1 一步回归的困境 ----------
CH = "13"
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.1))
z = np.array([-2.2, 0.0])
ends = [np.array([1.1, 0.75]), np.array([1.1, -0.75])]
for e, c in zip(ends, [BLUE, GREEN]):
    ax.annotate("", xy=e, xytext=z, arrowprops=dict(arrowstyle="-|>", color=c, lw=1.1,
                                                    connectionstyle="arc3,rad=0.25"))
    ax.scatter(*e, s=24, c=c, zorder=4)
ax.scatter(*z, s=28, c="#9a9a9a", zorder=4)
ax.text(z[0] - 0.15, z[1] - 0.42, "一个噪声点", fontsize=8.2, color=GRAY, ha="center")
mid = 0.5 * (ends[0] + ends[1])
ax.scatter(*mid, s=32, c=RED, marker="x", lw=1.6, zorder=5)
ax.annotate("一步回归落在均值", mid, xytext=(mid[0] + 0.15, mid[1] - 0.62), fontsize=8.2,
            color=RED, ha="center", arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.set_xlim(-2.8, 2.2)
ax.set_ylim(-1.7, 1.7)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig13_blur", CH)

# ---------- 图 14.1 保真与可编辑 ----------
CH = "19"
t = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.1))
ax.plot(t, 1 - 0.55 * t ** 1.6, color=BLUE, lw=1.4, label="保真度")
ax.plot(t, 0.15 + 0.8 * t ** 1.2, color=RED, lw=1.4, label="对齐度")
ax.axvspan(0.35, 0.7, color=LIGHT, alpha=0.5, lw=0)
ax.text(0.525, 0.05, "可用区间", ha="center", fontsize=8.0, color=GRAY)
ax.set_xlabel("编辑强度")
ax.set_ylabel("相对指标")
ax.set_ylim(0, 1.12)
ax.set_yticks([])
ax.legend(loc="center right", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig19_tradeoff", CH)

# ---------- 图 15.1 三种反演 ----------
CH = "15"
fig, ax = plt.subplots(figsize=(W_FULL, 2.05))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")


def box(x, y, w, h, label, fc="#eef2f6", ec=BLUE, fs=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK)


box(0.3, 3.6, 1.5, 1.0, "图像 $x$")
box(3.0, 3.6, 2.7, 1.0, "优化 $z$（慢，准）")
box(3.0, 2.1, 2.7, 1.0, "编码器（快，粗）")
box(3.0, 0.6, 2.7, 1.0, "编码器 + 优化")
box(6.8, 2.35, 1.4, 1.4, "$z$", fc="#fdf3e3", ec=SAND)
for y in (4.1, 2.6, 1.1):
    ax.annotate("", xy=(2.95, y), xytext=(1.85, y), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
    ax.annotate("", xy=(6.75, 3.05), xytext=(5.75, y), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
box(9.0, 2.35, 2.5, 1.4, "编辑后重建", fc="#f2f2f0", ec=GRAY)
ax.annotate("", xy=(8.95, 3.05), xytext=(8.25, 3.05), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
save(fig, "fig15_inversion", CH)

# ---------- 图 15.2 SDEdit ----------
t0 = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.05))
ax.plot(t0, 1 - 0.85 * t0 ** 1.1, color=BLUE, lw=1.4, label="与原图相似")
ax.plot(t0, 0.05 + 0.9 * t0 ** 1.5, color=RED, lw=1.4, label="与目标条件一致")
ax.axvline(0.55, color=GRAY, lw=0.7, ls=(0, (4, 3)))
ax.text(0.57, 0.78, "常用 $t_0$", fontsize=8.0, color=GRAY)
ax.set_xlabel("$t_0$")
ax.set_ylabel("相对指标")
ax.set_ylim(0, 1.1)
ax.set_yticks([])
ax.legend(loc="center right", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig15_sdedit", CH)

# ---------- 图 16.1 注意力替换 ----------
CH = "16"
g = 10


def blob(cy, cx, sy, sx):
    yy, xx = np.mgrid[0:g, 0:g]
    return np.exp(-((yy - cy) ** 2 / (2 * sy ** 2) + (xx - cx) ** 2 / (2 * sx ** 2)))


src = blob(4.5, 4.0, 2.0, 1.5)
tgt = blob(4.5, 5.2, 2.6, 2.2)
fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.75), gridspec_kw=dict(wspace=0.08))
for ax, im in zip(axes, [src, tgt, src]):
    ax.imshow(im, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig16_attn", CH)

# ---------- 图 17.1 ControlNet ----------
CH = "17"
fig, ax = plt.subplots(figsize=(W_FULL, 2.25))
ax.set_xlim(0, 12.5)
ax.set_ylim(0, 6)
ax.axis("off")


def box2(x, y, w, h, label, fc="#eef2f6", ec=BLUE, ls="-", fs=7.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9, ls=ls))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK)


box2(0.4, 3.6, 2.0, 1.2, "冻结编码器", fc="#f4f4f2", ls=(0, (3, 2)))
box2(0.4, 1.0, 2.0, 1.2, "可训练副本", fc="#e8eff6")
box2(3.2, 3.6, 1.5, 1.2, "中间层", fc="#f4f4f2")
box2(3.2, 1.0, 1.5, 1.2, "零卷积", fc="#fdf3e3", ec=SAND)
box2(5.4, 2.2, 1.1, 1.9, "相加", fc="#ffffff", ec=GRAY)
box2(7.4, 2.2, 2.0, 1.9, "解码器", fc="#f4f4f2")
ax.annotate("", xy=(2.45, 4.2), xytext=(2.45, 4.9), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
ax.annotate("", xy=(2.45, 1.6), xytext=(2.45, 0.5), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
ax.annotate("", xy=(3.15, 4.2), xytext=(2.45, 4.2), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(3.15, 1.6), xytext=(2.45, 1.6), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(5.35, 3.1), xytext=(4.75, 3.1), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(5.35, 3.1), xytext=(4.75, 1.6), arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9,
                                                                    connectionstyle="arc3,rad=-0.2"))
ax.annotate("", xy=(7.35, 3.1), xytext=(6.55, 3.1), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.text(0.4, 5.15, "含噪图", fontsize=7.0, color=GRAY)
ax.text(0.4, 0.55, "条件图", fontsize=7.0, color=GRAY)
ax.text(4.05, 0.6, "零初始化", fontsize=6.8, color=SAND)
save(fig, "fig17_controlnet", CH)

# ---------- 图 17.2 反演漂移 ----------
t = np.linspace(0, 1, 200)
true = 0.9 * np.cos(2.2 * t) + 0.1
inv = true + 0.18 * t ** 2.2
fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.1))
ax.plot(t, true, color=RED, lw=1.4, label="真实前向轨迹")
ax.plot(t, inv, color=BLUE, lw=1.4, label="反演轨迹")
ax.fill_between(t, true, inv, color=BLUE, alpha=0.12, lw=0)
ax.set_xlabel("$t$")
ax.set_ylabel("$x_t$（某一维）")
ax.legend(loc="lower left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig17_drift", CH)

# ---------- 图 18.1 受控 ODE ----------
CH = "18"
fig, ax = plt.subplots(figsize=(W_FULL * 0.66, 2.2))
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
ax.legend(loc="upper left", fontsize=7.2)
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right"))
save(fig, "fig18_rf", CH)

# ---------- 图 18.2 噪声水平 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.88, 1.95))
tt = np.linspace(0, 1, 200)
ax.plot(tt, np.minimum(1, 2 * tt), color=BLUE, lw=1.5, label="先反演再生成")
ax.plot(tt, 0.05 * np.ones_like(tt), color=RED, lw=1.5, label="免反演的直接路径")
ax.set_xlabel("过程进度")
ax.set_ylabel("噪声水平")
ax.set_ylim(0, 1.1)
ax.legend(loc="center right", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig18_fe", CH)

# ---------- 图 18.3 drift 与平滑 ----------
rng = np.random.default_rng(7)
xs = np.linspace(0, 6, 26)
raw = 0.55 * np.sin(2.4 * xs) + 0.35 * rng.normal(0, 1, len(xs)) + 0.9
smooth = np.convolve(raw, np.ones(5) / 5, mode="same")
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 1.9), gridspec_kw=dict(wspace=0.3))
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
save(fig, "fig18_drift", CH)
