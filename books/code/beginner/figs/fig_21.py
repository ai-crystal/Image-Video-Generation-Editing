import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "21"

# ---------- 图 21.1 注意力替换 ----------
g = 14
yy, xx = np.mgrid[0:g, 0:g]


def blob(cy, cx, sy, sx):
    z = np.exp(-((yy - cy) ** 2 / (2 * sy ** 2) + (xx - cx) ** 2 / (2 * sx ** 2)))
    return z / z.sum()


src = blob(7.0, 5.0, 2.1, 1.9)          # 源提示词里“猫”落在左侧
tgt = blob(6.0, 9.0, 3.2, 3.0)          # 目标提示词自己算出的“狗”偏右且更散
fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.85), gridspec_kw=dict(wspace=0.10))
for ax, im, lab in zip(axes, [src, tgt, src], ["源“猫”", "目标“狗”", "替换后"]):
    ax.imshow(im, cmap="Blues", vmin=0, vmax=im.max())
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(g * 0.5, g + 1.0, lab, ha="center", fontsize=8.2, color=GRAY)
    for s in ax.spines.values():
        s.set_color(LIGHT)
axes[0].annotate("", xy=(4.0, 7.0), xytext=(7.6, 5.6),
                 arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0,
                                 connectionstyle="arc3,rad=0.25"))
axes[0].text(8.4, 3.0, "复制这一列", fontsize=7.4, color=RED)
save(fig, "fig21_attn", CH)

# ---------- 图 21.2 替换窗口 ----------
f = np.linspace(0, 1, 200)
layout = 1 - 0.78 * f ** 0.85
sem = 0.06 + 0.86 * f ** 1.35
fig, ax = plt.subplots(figsize=(W_FULL * 0.82, 2.2))
ax.plot(f, layout, color=BLUE, lw=1.5, label="布局一致性")
ax.plot(f, sem, color=RED, lw=1.5, label="语义对齐度")
ax.axvspan(0.2, 0.5, color=LIGHT, alpha=0.55, lw=0)
ax.text(0.35, 0.94, "常用窗口", ha="center", fontsize=8.0, color=GRAY)
ax.set_xlabel("替换步数占总步数的比例")
ax.set_ylabel("相对指标（定性示意）")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.12)
ax.set_yticks([])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=8.0)
style(ax, spines=("top", "right"))
save(fig, "fig21_steps", CH)

# ---------- 图 21.3 mask 边界的潜空间过渡带 ----------
npix = 256
lat = npix // 8
m_pix = (np.arange(npix) >= 128).astype(float)
m_lat = m_pix.reshape(lat, 8).mean(axis=1)          # 8 倍下采样
x_lat = (np.arange(lat) + 0.5) * 8 - 0.5
x_pix = np.arange(npix)
m_up = np.interp(x_pix, x_lat, m_lat)               # 线性插值回像素
fig, ax = plt.subplots(figsize=(W_FULL * 0.88, 1.95))
ax.step(x_pix, m_pix, where="mid", color=LIGHT, lw=1.6, label="像素空间二值 mask")
ax.plot(x_pix, m_up, color=BLUE, lw=1.5, label="经潜空间再解码")
ax.plot(x_lat, m_lat, "o", ms=3.4, color=RED, label="潜空间取值（8 倍下采样）")
ax.axvspan(120, 136, color=SAND, alpha=0.18, lw=0)
ax.text(128, 1.06, "过渡带约一格", ha="center", fontsize=7.8, color=GRAY)
ax.set_xlabel("图像横向坐标（像素）")
ax.set_ylabel("mask 取值")
ax.set_xlim(80, 176)
ax.set_ylim(-0.06, 1.2)
ax.legend(loc="lower right", fontsize=7.6)
style(ax, spines=("top", "right"))
save(fig, "fig21_mask", CH)
