import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 9.2 抖动的时间频率分布与人的敏感度 ----------
CH = "09"
FS = 24.0                      # 帧率
f = np.linspace(1e-4, FS / 2, 1200)
w = 2 * np.pi * f / FS

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.05), gridspec_kw=dict(wspace=0.36))

# 左：三类抖动的时间功率谱，横轴 Hz，纵轴归一到“独立采样在带宽内的均值为 1”
ax = axes[0]
S_ind = 2 * np.sin(w / 2) ** 2                     # 独立采样：sin^2(pi f/FS) 形状，均值为 1
rho = 0.9
S_sh = (1 - rho) * S_ind                           # 共享九成噪声：同形，幅度缩放

a = 0.87                                           # 慢变参数：AR(1)，相关时间约 0.3 s
z = np.exp(-1j * w)
S_theta = 1.0 / np.abs(1 - a * z) ** 2             # 参数过程的谱
S_dr = 4 * np.sin(w / 2) ** 2 * S_theta            # 差分后的谱
area = np.trapezoid(S_dr, f)
S_dr = S_dr / area * (FS / 2.0)                    # 归一到与独立采样相同的总功率

ax.plot(f, S_ind, color=RED, lw=1.5, label=r"逐帧独立采样")
ax.plot(f, S_dr, color=BLUE, lw=1.5, label="参数慢变（0.3 秒）")
ax.plot(f, S_sh, color=GRAY, lw=1.3, ls="--", label="共享九成噪声")
ax.axvline(FS / 2, color=LIGHT, lw=0.9, zorder=0)
ax.set_xlabel("时间频率（Hz）")
ax.set_ylabel("归一化功率谱")
ax.set_xlim(0, FS / 2 + 0.2)
ax.set_ylim(0, 2.55)
ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
ax.set_xticks([0, 3, 6, 9, 12])
ax.legend(loc="upper left", handlelength=1.6, labelspacing=0.32, fontsize=7.4)
style(ax, grid=True)

# 右：时域对比敏感度的定性形状（示意，不对应具体实测曲线）
ax = axes[1]
fp = 7.0
fc = np.linspace(0.2, 34, 600)
C = (fc / fp) * np.exp(1 - fc / fp)
ax.axvspan(0, 12, color=SAND, alpha=0.16, lw=0, zorder=0)
ax.plot(fc, C, color=INK, lw=1.3)
ax.axvline(12, color=GRAY, lw=0.9, ls=":")
ax.set_xlabel("时间频率（Hz）")
ax.set_ylabel("相对敏感度（定性）")
ax.set_xlim(0, 34)
ax.set_ylim(0, 1.24)
ax.set_yticks([0, 0.5, 1.0])
ax.annotate("峰值约 7 Hz", xy=(7.3, 1.0), xytext=(15.0, 1.09),
            fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle="-", lw=0.8, color=GRAY,
                            shrinkA=2, shrinkB=3))
ax.text(3.3, 0.06, "24 fps 的采样带宽", fontsize=7.6, color=GRAY, va="bottom")
style(ax)

save(fig, "fig09_tempspec", CH)
