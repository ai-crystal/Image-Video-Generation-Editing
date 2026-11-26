import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "01"

# ---------- 图 1.2 编辑类型在"新内容 x 结构位移"平面上的位置 ----------
fig, ax = plt.subplots(figsize=(W_FULL * 0.92, 2.8))

pts = [
    ("换颜色", 0.09, 0.08, BLUE, (0.03, 0.03)),
    ("换材质", 0.36, 0.23, BLUE, (0.03, 0.03)),
    ("换季节", 0.25, 0.40, BLUE, (0.03, 0.03)),
    ("换画风", 0.63, 0.26, SAND, (0.03, 0.03)),
    ("换同类物体", 0.63, 0.43, GREEN, (0.03, 0.03)),
    ("加/删物体", 0.85, 0.68, GREEN, (0.03, 0.03)),
    ("换姿态", 0.52, 0.83, RED, (0.03, 0.04)),
    ("换视角", 0.80, 0.93, RED, (0.03, 0.04)),
    ("文字渲染", 0.86, 0.13, GREEN, (-0.14, -0.09)),
]
for name, x, y, c, off in pts:
    ax.plot(x, y, "o", ms=5.2, mfc=c, mec="white", mew=0.7, zorder=3)
    ax.annotate(name, (x, y), xytext=(x + off[0], y + off[1]), fontsize=7.8, color=INK)

# 等难度线：0.55 * 新内容 + 0.85 * 结构改动
xx = np.linspace(0, 1.02, 200)
for D in (0.35, 0.75, 1.15):
    yy = (D - 0.55 * xx) / 0.85
    m = (yy >= 0) & (yy <= 1.0)
    ax.plot(xx[m], yy[m], ls=(0, (3, 3)), color=LIGHT, lw=1.0, zorder=1)

ax.set_xlim(0, 1.02)
ax.set_ylim(0, 1.02)
ax.set_xlabel("需要新生成的内容")
ax.set_ylabel("结构改动量")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right"))
save(fig, "fig01_types", CH)
