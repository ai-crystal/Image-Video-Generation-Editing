import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 13.2 三种注意力组织的计算量 ----------
CH = "13"
d = 320
T = 16
configs = [
    ("$N=4096$", 4096),
    ("$N=256$", 256),
]
names = ["全局时空", "空间（逐帧）", "时间（逐位置）"]
colors = [RED, BLUE, GREEN]

fig, ax = plt.subplots(figsize=(W_FULL * 0.72, 2.4))
x = np.arange(len(configs))
w = 0.26
vals = {}
for N in [4096, 256]:
    vals[N] = [
        2 * (N * T) ** 2 * d / 1e9,
        2 * N ** 2 * T * d / 1e9,
        2 * T ** 2 * N * d / 1e9,
    ]
for j, (name, c) in enumerate(zip(names, colors)):
    ys = [vals[N][j] for N in [4096, 256]]
    ax.bar(x + (j - 1) * w, ys, width=w, color=c, label=name)
    for i, y in enumerate(ys):
        ax.text(i + (j - 1) * w, y * 1.35, ("%.3g" % y), ha="center", fontsize=7.0, color=INK)
ax.set_yscale("log")
ax.set_ylim(1e-2, 2e4)
ax.set_xticks(x)
ax.set_xticklabels(["$N=4096$（$64\\times64$）", "$N=256$（$16\\times16$）"])
ax.set_ylabel("乘加次数（G，$T=16$）")
ax.legend(loc="upper right", ncol=1)
style(ax, grid=True)
ax.grid(axis="x", visible=False)
save(fig, "fig13_cost", CH)

# ---------- 图 13.3 显存随帧数的增长 ----------
CH = "13"
T = np.arange(4, 97)
C = 320
H = W = 64
one_frame = C * H * W * 4 / 1024 ** 3           # 一帧特征，GB
feat = one_frame * T                            # 单份 T 帧特征
acts = feat * 40                                # 反向传播保留约 40 份
attn = 8 * (H * W) ** 2 * T * 4 / 1024 ** 3     # 8 头空间注意力矩阵

fig, ax = plt.subplots(figsize=(W_FULL * 0.72, 2.4))
ax.plot(T, feat, color=BLUE_L, label="一份 $64\\times64\\times320$ 特征")
ax.plot(T, acts, color=BLUE, label="反向传播保留的 40 份激活")
ax.plot(T, attn, color=RED, label="8 头空间注意力矩阵")
ax.axhline(24, color=GRAY, lw=0.8, ls=(0, (4, 3)))
ax.text(78, 26, "24 GB", fontsize=7.4, color=GRAY)
ax.set_yscale("log")
ax.set_xlabel("帧数 $T$")
ax.set_ylabel("显存（GB）")
ax.set_ylim(1e-2, 1e3)
ax.legend(loc="upper left")
style(ax, grid=True)
save(fig, "fig13_memory", CH)
