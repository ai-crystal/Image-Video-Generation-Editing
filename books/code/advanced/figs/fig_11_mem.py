import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"

# 720p、16 帧每秒、潜空间 8x8 空间下采样、4 倍时间下采样、16 通道、宽度 1536、bf16
H, W, FPS = 720, 1280, 16
CS, FS, TS, DIM, BYTES = 16, 8, 4, 1536, 2

dur = np.linspace(1.0, 12.0, 200)
F = dur * FPS
lf = F / TS
lh, lw = H // FS, W // FS
latent = CS * lf * lh * lw * BYTES
tokens = lf * lh * lw
act = tokens * DIM * BYTES
attn = tokens ** 2 * BYTES

fig, ax = plt.subplots(figsize=(W_FULL, 2.6))
ax.loglog(dur, attn / 2 ** 30, color=RED, lw=1.6, label="全 3D 注意力（单头）")
ax.loglog(dur, act / 2 ** 30, color=BLUE, lw=1.6, label="单层激活（token 向量）")
ax.loglog(dur, latent / 2 ** 30, color=GREEN, lw=1.6, label="潜变量张量本身")

ax.axhline(80, color=GRAY, lw=0.9, ls="--")
ax.text(11.6, 92, "80 GB", fontsize=8, color=GRAY, ha="right")

ax.set_xlabel("片段时长（秒，16 帧每秒）")
ax.set_ylabel("显存（GB，bf16，单样本）")
ax.set_xticks([1, 2, 5, 10])
ax.set_xticklabels(["1", "2", "5", "10"])
ax.set_yticks([1e-3, 1e-1, 1e1, 1e3])
ax.set_xlim(1, 12)
ax.set_ylim(1e-3, 1e4)
style(ax, grid=True)
ax.legend(loc="upper left", ncol=1)
save(fig, "fig11_mem", CH)
