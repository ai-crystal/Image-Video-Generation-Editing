import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "01"

# ---------- 图 1.3 mask 收缩对背景 PSNR 的影响 ----------
# 假设：512x512 图，圆盘 mask 覆盖 5%，外溢误差按 delta * exp(-d / d0) 向 mask 外衰减，
# d 为到 mask 边界的距离（像素），d0 = 2。把 mask 向内收缩 k 像素，等于把 d < k 的误差从统计里剔掉。
S = 512
HW = S * S
r0 = np.sqrt(0.05 * HW / np.pi)
perim = 2 * np.pi * r0
d0 = 2.0

k = np.arange(0, 4.01, 0.05)
fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.5))
for delta, c, lab in ((0.2, BLUE, r"外溢幅度 0.20"),
                      (0.35, SAND, r"外溢幅度 0.35"),
                      (0.5, RED, r"外溢幅度 0.50")):
    mse = perim * delta ** 2 * d0 / (2 * HW) * np.exp(-2 * k / d0)
    ax.plot(k, -10 * np.log10(mse), color=c, lw=1.4, label=lab)

ax.axhline(40, color=GRAY, lw=0.7, ls=(0, (4, 3)))
ax.text(0.06, 40.6, "40 dB", fontsize=7.6, color=GRAY)
ax.set_xlabel("mask 向内收缩的像素数 $k$")
ax.set_ylabel("背景 PSNR (dB)")
ax.set_xlim(0, 4)
ax.set_ylim(32, 61)
ax.set_xticks([0, 1, 2, 3, 4])
ax.legend(loc="upper left", fontsize=7.8, ncol=1)
ax.annotate("每收缩 1 像素\n约 +4.3 dB", xy=(2.0, 50.8), xytext=(2.35, 36.4),
            fontsize=7.6, color=GRAY,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.7, ls=(0, (3, 2))))
style(ax, spines=("top", "right"))
save(fig, "fig01_mask", CH)
