import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "05"

# ---------- 图 5.2 笔刷 mask 的潜空间下采样 ----------
H = 256
yy, xx = np.mgrid[0:H, 0:H].astype(float)


def stroke(y0, amp, freq, thick, phase=0.0):
    yc = y0 + amp * np.sin(freq * 2 * np.pi * xx / H + phase)
    return (np.abs(yy - yc) < thick).astype(float)


m = np.clip(stroke(60, 28, 1.5, 1.0) + stroke(135, 22, 1.0, 1.0, 1.4)
            + stroke(205, 18, 2.0, 1.2, 2.6), 0, 1)

# 8x 平均池化
low = m.reshape(H // 8, 8, H // 8, 8).mean(axis=(1, 3))
low_up = np.kron(low, np.ones((8, 8)))
hard = np.kron((low > 0.5).astype(float), np.ones((8, 8)))
print("原覆盖率 %.3f   下采样最大覆盖率 %.3f   阈值0.5后覆盖率 %.3f"
      % (m.mean(), low.max(), hard.mean()))

fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.62), gridspec_kw=dict(wspace=0.06))
for ax, im, vmax in [(axes[0], m, 1.0), (axes[1], low_up, 0.40), (axes[2], hard, 1.0)]:
    ax.imshow(im, cmap="Blues", vmin=0, vmax=vmax, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(LIGHT)
axes[0].set_xlabel("像素级掩码", fontsize=8.4)
axes[1].set_xlabel("8× 池化覆盖率（峰值 0.36）", fontsize=8.4)
axes[2].set_xlabel("阈值 0.5 后再上采样", fontsize=8.4)
save(fig, "fig05_mask", CH)

# ---------- 图 5.3 条件冲突：合成幅度与夹角 ----------
th = np.linspace(0, np.pi, 400)
fig, ax = plt.subplots(figsize=(W_FULL * 0.78, 2.15))
for w, c, lab in [(1.0, BLUE, "等权 $w_2=1$"), (0.6, SAND, "$w_2=0.6$"),
                  (0.3, GRAY, "$w_2=0.3$")]:
    ax.plot(np.degrees(th), np.sqrt(1 + w ** 2 + 2 * w * np.cos(th)), color=c, lw=1.4, label=lab)
ax.axhline(1.0, color=RED, lw=0.8, ls=(0, (4, 3)))
ax.text(4, 1.03, "单条件强度", fontsize=7.6, color=RED)
ax.axvline(120, color=LIGHT, lw=0.7)
ax.plot([120], [1.0], "o", ms=4.5, color=INK, zorder=5)
ax.annotate("$120°$：等权时回到 1", xy=(120, 1.0), xytext=(126, 1.36), fontsize=7.6,
            color=INK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.set_xlabel("两个条件修正量的夹角（度）")
ax.set_ylabel("合成幅度 / 单条件")
ax.set_xlim(0, 180)
ax.set_ylim(0, 2.1)
ax.set_xticks([0, 45, 90, 120, 180])
ax.legend(loc="lower left", fontsize=7.8)
style(ax, spines=("top", "right"))
save(fig, "fig05_conflict", CH)
