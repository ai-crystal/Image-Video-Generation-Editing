import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "24"

rng = np.random.default_rng(0)

# 合成算例：一段缓慢平移的纹理，叠加逐帧独立的亮度抖动
H = W = 96
T = 16
yy, xx = np.mgrid[0:H, 0:W]
base = 128.0 + 60.0 * np.sin(2 * np.pi * xx / 48.0) + 40.0 * np.sin(2 * np.pi * yy / 64.0 + 0.7)


def frames(sigma):
    out = []
    for t in range(T):
        img = np.roll(base, t, axis=1)  # 每帧平移 1 像素（整数，回滚精确）
        img = img + rng.normal(0.0, sigma, size=img.shape)
        out.append(img)
    return out


def diffs(sigma):
    fr = frames(sigma)
    naive, warped = [], []
    for t in range(T - 1):
        a, b = fr[t], fr[t + 1]
        naive.append(np.mean(np.abs(b - a)))
        # 光流已知（整像素平移 1），补偿后比较
        b_back = np.roll(b, -1, axis=1)
        warped.append(np.mean(np.abs(b_back - a)))
    return np.mean(naive), np.mean(warped)


sigmas = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0])
res = np.array([diffs(s) for s in sigmas])

fig, ax = plt.subplots(figsize=(W_FULL, 2.6))
ax.plot(sigmas, res[:, 0], "o-", color=RED, ms=4, label="不做运动补偿：帧间差")
ax.plot(sigmas, res[:, 1], "s-", color=BLUE, ms=4, label="补偿运动后：残差")
ax.fill_between(sigmas, res[:, 1], res[:, 0], color=LIGHT, alpha=0.55, lw=0)

ax.set_xlabel("逐帧抖动幅度 $\\sigma$（灰度级，0–255 尺度）")
ax.set_ylabel("平均绝对残差（灰度级）")
ax.set_ylim(0, 12)
ax.annotate("同一段抖动，上面这条几乎不动\n下面这条按 $1.13\\,\\sigma$ 上升",
            xy=(4.6, 7.0), xytext=(1.85, 9.7), fontsize=8.2, color=GRAY,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
ax.legend(loc="lower right")
style(ax, grid=True)
save(fig, "fig24_warp", CH)
