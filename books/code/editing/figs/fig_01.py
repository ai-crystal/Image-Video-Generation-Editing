import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ---------- 图 1.1 保真与可编辑 ----------
CH = "01"
t = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.15))
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
save(fig, "fig01_tradeoff", CH)

# ---------- 图 2.1 三种反演 ----------
CH = "02"
fig, ax = plt.subplots(figsize=(W_FULL, 2.1))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")


def box(x, y, w, h, label, fc="#eef2f6", ec=BLUE, fs=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK)


box(0.3, 3.6, 1.5, 1.0, "图像 $x$")
box(3.0, 3.6, 2.6, 1.0, "优化 $z$（慢，准）")
box(3.0, 2.1, 2.6, 1.0, "编码器 $E(x)$（快，粗）")
box(3.0, 0.6, 2.6, 1.0, "编码器 + 优化")
box(6.7, 2.35, 1.5, 1.4, "$z$", fc="#fdf3e3", ec=SAND)
for y in (4.1, 2.6, 1.1):
    ax.annotate("", xy=(2.95, y), xytext=(1.85, y), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
    ax.annotate("", xy=(6.65, 3.05), xytext=(5.65, y), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
box(8.9, 2.35, 2.6, 1.4, "编辑后重建", fc="#f2f2f0", ec=GRAY)
ax.annotate("", xy=(8.85, 3.05), xytext=(8.25, 3.05), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
save(fig, "fig02_inversion", CH)

# ---------- 图 2.2 SDEdit ----------
t0 = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.1))
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
save(fig, "fig02_sdedit", CH)

# ---------- 图 3.1 注意力替换 ----------
CH = "03"
g = 10


def blob(cy, cx, sy, sx):
    yy, xx = np.mgrid[0:g, 0:g]
    return np.exp(-((yy - cy) ** 2 / (2 * sy ** 2) + (xx - cx) ** 2 / (2 * sx ** 2)))


src = blob(4.5, 4.0, 2.0, 1.5)
tgt = blob(4.5, 5.2, 2.6, 2.2)
fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.8), gridspec_kw=dict(wspace=0.08))
for ax, im in zip(axes, [src, tgt, src]):
    ax.imshow(im, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(LIGHT)
save(fig, "fig03_attn", CH)

# ---------- 图 4.1 反演漂移 ----------
CH = "04"
fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.2))
t = np.linspace(0, 1, 200)
true = 0.9 * np.cos(2.2 * t) + 0.1
inv = true + 0.18 * t ** 2.2
ax.plot(t, true, color=RED, lw=1.4, label="真实前向轨迹")
ax.plot(t, inv, color=BLUE, lw=1.4, label="DDIM 反演轨迹")
ax.fill_between(t, true, inv, color=BLUE, alpha=0.12, lw=0)
ax.set_xlabel("$t$")
ax.set_ylabel("$x_t$（某一维）")
ax.legend(loc="lower left", fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig04_drift", CH)

# ---------- 图 4.2 EDICT ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.2))
n = 8
x = np.array([0.0, 0.0])
y = np.array([0.25, -0.15])
xs, ys = [x.copy()], [y.copy()]
for i in range(n):
    x = x + np.array([0.55, 0.32]) + 0.08 * np.array([np.sin(i), np.cos(i)])
    y = y + np.array([0.50, 0.30]) + 0.08 * np.array([np.cos(i), np.sin(i)])
    xs.append(x.copy())
    ys.append(y.copy())
xs, ys = np.array(xs), np.array(ys)
ax.plot(xs[:, 0], xs[:, 1], "o-", color=BLUE, ms=3, lw=0.9, label="轨迹 $x_t$")
ax.plot(ys[:, 0], ys[:, 1], "s--", color=RED, ms=3, lw=0.9, label="轨迹 $y_t$")
for i in range(0, n, 2):
    ax.annotate("", xy=(xs[i + 1, 0], xs[i + 1, 1]), xytext=(ys[i, 0], ys[i, 1]),
                arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.7,
                                connectionstyle="arc3,rad=0.2"))
ax.set_xlabel("$z_1$")
ax.set_ylabel("$z_2$")
ax.legend(loc="upper left", fontsize=7.6)
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right"))
save(fig, "fig04_edict", CH)

# ---------- 图 5.1 ControlNet ----------
CH = "05"
fig, ax = plt.subplots(figsize=(W_FULL, 2.35))
ax.set_xlim(0, 12.5)
ax.set_ylim(0, 6)
ax.axis("off")


def box2(x, y, w, h, label, fc="#eef2f6", ec=BLUE, ls="-", fs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=0.9, ls=ls))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK)


box2(0.4, 3.6, 2.0, 1.2, "冻结编码器", fc="#f4f4f2", ls=(0, (3, 2)))
box2(0.4, 1.0, 2.0, 1.2, "可训练副本", fc="#e8eff6")
box2(3.2, 3.6, 1.5, 1.2, "中间层", fc="#f4f4f2")
box2(3.2, 1.0, 1.5, 1.2, "零卷积", fc="#fdf3e3", ec=SAND)
box2(5.4, 2.2, 1.1, 1.9, "相加", fc="#ffffff", ec=GRAY)
box2(7.4, 2.2, 2.0, 1.9, "解码器", fc="#f4f4f2")
box2(0.4, 5.2, 2.0, 0.6, "含噪图 $z_t$", fc="#ffffff", ec=GRAY, fs=6.8)
box2(0.4, -0.2, 2.0, 0.6, "条件图", fc="#ffffff", ec=GRAY, fs=6.8)
ax.annotate("", xy=(2.45, 4.2), xytext=(2.45, 5.2), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
ax.annotate("", xy=(2.45, 1.6), xytext=(2.45, 0.4), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))
ax.annotate("", xy=(3.15, 4.2), xytext=(2.45, 4.2), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(3.15, 1.6), xytext=(2.45, 1.6), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(5.35, 3.1), xytext=(4.75, 3.1), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(5.35, 3.1), xytext=(4.75, 1.6), arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9,
                                                                    connectionstyle="arc3,rad=-0.2"))
ax.annotate("", xy=(7.35, 3.1), xytext=(6.55, 3.1), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.text(4.05, 0.55, "零初始化", fontsize=6.8, color=SAND)
save(fig, "fig05_controlnet", CH)
