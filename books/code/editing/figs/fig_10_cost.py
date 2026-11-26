import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 10.2 时空注意力的两种分解的代价 ----------
CH = "10"
HW = 64 * 64          # 隐空间空间分辨率
D = 64                # 单个头的通道数
Ls = np.arange(2, 65)

full = (Ls * HW) ** 2 * D                      # 全三维：帧与位置一起算注意力
decomp = Ls * HW ** 2 * D + HW * Ls ** 2 * D   # 空间层 + 时间层

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.1), gridspec_kw=dict(wspace=0.36))

ax = axes[0]
ax.semilogy(Ls, full, color=RED, lw=1.4, label="全三维")
ax.semilogy(Ls, decomp, color=BLUE, lw=1.4, label="空间 + 时间两层")
ax.set_xlabel("帧数 $L$")
ax.set_ylabel("计算量（乘加次数）")
ax.set_xlim(2, 64)
ax.set_ylim(1e9, 1e13)
ax.legend(loc="lower right", handlelength=1.5)
style(ax, grid=True)

ax = axes[1]
ax.semilogy(Ls, (Ls * HW) ** 2 * 2 / 1e9, color=RED, lw=1.4, label="全三维")
ax.semilogy(Ls, Ls * HW ** 2 * 2 / 1e9, color=BLUE, lw=1.4, label="空间层")
ax.axhline(24, color=GRAY, lw=0.8, ls=(0, (4, 3)))
ax.text(4, 30, "单卡上限（量级）", fontsize=7.2, color=GRAY)
ax.set_xlabel("帧数 $L$")
ax.set_ylabel("注意力矩阵显存（GB，单头单层）")
ax.set_xlim(2, 64)
ax.set_ylim(1e-2, 1e3)
ax.legend(loc="lower right", handlelength=1.5)
style(ax, grid=True)

save(fig, "fig10_cost", CH)
