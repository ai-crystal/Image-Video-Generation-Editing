import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"

# 5 秒片段；潜空间 8x8 空间下采样、4 倍时间下采样、宽度 1536、30 层
T = 5.0
DIM, LAYERS, FS, TS = 1536, 30, 8, 4
EFF = 0.4  # 有效算力占峰值比例
PEAK_PFLOP = 1.0  # bf16 峰值 1000 TFLOPS，折成 PFLOP/s

res = [("480p", 480, 640), ("720p", 720, 1280), ("1080p", 1080, 1920)]
fps = [8, 16, 24]

pp = np.zeros((len(fps), len(res)))   # PFLOP
for j, (name, H, W) in enumerate(res):
    lh, lw = H // FS, W // FS
    for i, f in enumerate(fps):
        s = (T * f / TS) * lh * lw
        pp[i, j] = 4 * s ** 2 * DIM * LAYERS / 1e15

sec = pp / (PEAK_PFLOP * EFF)

fig, ax = plt.subplots(figsize=(W_FULL, 2.7))
x = np.arange(len(res))
wbar = 0.26
colors = [GREEN, BLUE, RED]
for i, f in enumerate(fps):
    bars = ax.bar(x + (i - 1) * wbar, pp[i] - 0.3, width=wbar * 0.92,
                  bottom=0.3, color=colors[i], label="%d 帧每秒" % f)
    for b, v, t in zip(bars, pp[i], sec[i]):
        ax.annotate("%.0f s" % t, xy=(b.get_x() + b.get_width() / 2, v),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7.2, color=INK)

ax.set_yscale("log")
ax.set_ylim(0.3, 650)
ax.set_xticks(x)
ax.set_xticklabels([r[0] for r in res])
ax.set_xlabel("分辨率（5 秒片段）")
ax.set_ylabel("单次前向的注意力算力（PFLOP）")
ax.set_yticks([1, 10, 100])
ax.set_yticklabels(["1", "10", "100"])
style(ax, grid=True)
ax.legend(loc="upper left", ncol=1, handlelength=1.2, labelspacing=0.35)
save(fig, "fig11_budget", CH)

for i, f in enumerate(fps):
    print(f, ["%.1f PFLOP" % v for v in pp[i]], ["%.0f s" % t for t in sec[i]])
