import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
from matplotlib.patches import FancyBboxPatch

# ---------- 图 25.1 三条选型分支 ----------
CH = "25"
fig, ax = plt.subplots(figsize=(W_FULL, 3.05))
ax.set_xlim(0, 9.0)
ax.set_ylim(0, 8.0)
ax.axis("off")


def box(x, y, w, h, label, fc, ec, fs=7.2, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.09",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=INK,
            linespacing=1.5)


rows = [
    ("从零出图", "要控\n布局吗",
     "否：直接采样，\n20–30 步", "是：加边缘、\n深度、姿态条件"),
    ("生成视频", "时长\n多少",
     "几秒：整段\n一次生成", "几十秒：分块，\n接受漂移"),
    ("改一张图", "改动\n多大",
     "小：噪声注入、\n潜空间方向", "中到大：注意力操作\n反演 + 条件"),
]
ys = [6.45, 4.05, 1.65]
for (entry, cond, leaf_up, leaf_dn), y in zip(rows, ys):
    box(0.10, y - 0.44, 1.78, 0.88, entry, "#eef2f6", BLUE, fs=7.4)
    box(2.30, y - 0.44, 2.05, 0.88, cond, "#fdf3e3", SAND, fs=7.2)
    ax.annotate("", xy=(2.24, y), xytext=(1.94, y),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9, mutation_scale=7))
    for label, dy in ((leaf_up, 0.52), (leaf_dn, -0.58)):
        box(5.00, y + dy - 0.38, 3.90, 0.76, label, "#f5f5f3", GRAY, fs=6.9)
        ax.annotate("", xy=(4.94, y + dy), xytext=(4.52, y),
                    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8, mutation_scale=7,
                                    connectionstyle="arc3,rad=%.2f" % (-0.30 if dy > 0 else 0.30)))
save(fig, "fig25_choice", CH)
