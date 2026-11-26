import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from scipy.ndimage import map_coordinates

# ---------- 图 10.3 内容场 + 形变场 = 帧 ----------
CH = "10"
H = W = 128
yy, xx = np.mgrid[0:H, 0:W].astype(float)

# 内容场：地面 + 太阳 + 一个带条纹的主体
C = np.zeros((H, W, 3))
C[..., 0] = 0.86
C[..., 1] = 0.90
C[..., 2] = 0.94
ground = yy > 86
C[ground] = np.array([0.80, 0.74, 0.60])

sun = (xx - 32) ** 2 + (yy - 30) ** 2 < 14 ** 2
C[sun] = np.array([0.85, 0.66, 0.28])

body = (xx - 78) ** 2 / 18 ** 2 + (yy - 74) ** 2 / 26 ** 2 < 1
stripe = (np.sin((xx - 78) * 0.9) > 0)
C[body & stripe] = np.array([0.42, 0.30, 0.26])
C[body & ~stripe] = np.array([0.70, 0.36, 0.30])

C = np.clip(C, 0, 1)


def deform(t):
    """返回形变后的采样坐标：F(p) = p + Δ_t(p)，含全局平移与一个旋转涡。"""
    dx, dy = 5.0 * t, -3.0 * t
    cx, cy = 78.0, 74.0
    r2 = (xx - cx) ** 2 + (yy - cy) ** 2
    w = np.exp(-r2 / (2 * 32.0 ** 2)) * (0.45 * t)
    ux = -(yy - cy) * w
    uy = (xx - cx) * w
    # map_coordinates 期望 (行, 列) 顺序，即 (y, x)
    return np.stack([yy + dy + uy, xx + dx + ux])


def render(t):
    co = deform(t)
    out = np.zeros_like(C)
    for k in range(3):
        out[..., k] = map_coordinates(C[..., k], co, order=1, mode="reflect")
    return np.clip(out, 0, 1)


fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.62), gridspec_kw=dict(wspace=0.06))
for ax in axes:
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

axes[0].imshow(C, extent=[0, W, H, 0], interpolation="nearest")
axes[0].text(4, 14, "内容场 $C$", fontsize=8, color=INK,
             bbox=dict(fc="white", ec="none", alpha=0.75, pad=1.5))

ax = axes[1]
ax.imshow(np.ones((H, W, 3)) * 0.97, extent=[0, W, H, 0], interpolation="nearest")
co = deform(1.0)
step = W // 8
for g in range(0, W, step):
    ax.plot(co[1, g, :], co[0, g, :], color=BLUE_L, lw=0.6)
    ax.plot(co[1, :, g], co[0, :, g], color=BLUE_L, lw=0.6)
ax.text(4, 14, "形变场 $F_t$", fontsize=8, color=INK,
        bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))

axes[2].imshow(render(1.0), extent=[0, W, H, 0], interpolation="nearest")
axes[2].text(4, 14, "第 $t$ 帧 $C(F_t)$", fontsize=8, color=INK,
             bbox=dict(fc="white", ec="none", alpha=0.75, pad=1.5))

save(fig, "fig10_codef", CH)
