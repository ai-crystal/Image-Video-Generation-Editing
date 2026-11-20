import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "01"

fig, ax = plt.subplots(figsize=(W_FULL, 3.35))
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 8.6)
ax.axis("off")

# 泳道标签
ax.text(0.28, 6.55, "图像", rotation=90, ha="center", va="center", fontsize=8.2, color=BLUE)
ax.text(0.28, 4.35, "视频", rotation=90, ha="center", va="center", fontsize=8.2, color=GREEN)
ax.text(0.28, 1.55, "编辑", rotation=90, ha="center", va="center", fontsize=8.2, color=RED)


def row(items, y, ec, fc, fs=6.3, w=1.8, h=0.9):
    for name, x in items:
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=fc, ec=ec, lw=0.9))
        ax.text(x, y, name, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.4)


gen = [("变分自编码器", 1.8), ("对抗网络", 3.95), ("扩散模型", 6.1), ("流模型", 8.25), ("一步生成", 10.4)]
row(gen, 6.9, BLUE, "#eef2f6")
for i in range(len(gen) - 1):
    ax.annotate("", xy=(gen[i + 1][1] - 0.93, 6.9), xytext=(gen[i][1] + 0.93, 6.9),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))

vid = [("时空 U-Net", 1.8), ("时间层", 3.95), ("3D VAE", 6.1), ("长视频", 8.25), ("视频编辑", 10.4)]
row(vid, 4.7, GREEN, "#eef5f0")
for i in range(len(vid) - 1):
    ax.annotate("", xy=(vid[i + 1][1] - 0.93, 4.7), xytext=(vid[i][1] + 0.93, 4.7),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8))

edit = [("隐空间", 1.8), ("噪声水平", 3.95), ("注意力", 6.1), ("结构条件", 8.25), ("反演与速度场", 10.4)]
row(edit, 1.55, RED, "#fbeeee")
for i in range(len(edit) - 1):
    ax.annotate("", xy=(edit[i + 1][1] - 0.93, 1.55), xytext=(edit[i][1] + 0.93, 1.55),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.7, alpha=0.6))

ax.plot([1.2, 11.6], [2.95, 2.95], color=LIGHT, lw=0.7, ls=(0, (4, 3)))
ax.text(6.4, 2.62, "编辑建立在生成模型之上：同一套网络，换一种用法", fontsize=6.9, color=GRAY, ha="center")

ax.plot([1.2, 11.6], [5.85, 5.85], color=LIGHT, lw=0.7, ls=(0, (4, 3)))
ax.text(6.4, 5.60, "视频在图像模型上加时间维，或者把整段帧压进潜空间", fontsize=6.9, color=GRAY, ha="center")

ax.text(6.4, 0.42, "箭头表示方法的承接，不严格对应年份；左右位置不代表难度。", fontsize=7.0, color=GRAY, ha="center")
save(fig, "fig01_map", CH)
