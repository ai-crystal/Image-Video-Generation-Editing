import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "01"


def euler_path(n, w, start=(1.0, 0.0)):
    x = np.array(start, float)
    h = 1.0 / n
    out = [x.copy()]
    for _ in range(n):
        x = x + h * w * np.array([-x[1], x[0]])
        out.append(x.copy())
    return np.array(out)


def heun_path(n, w, start=(1.0, 0.0)):
    x = np.array(start, float)
    h = 1.0 / n
    out = [x.copy()]
    for _ in range(n):
        k1 = w * np.array([-x[1], x[0]])
        y = x + h * k1
        k2 = w * np.array([-y[1], y[0]])
        x = x + 0.5 * h * (k1 + k2)
        out.append(x.copy())
    return np.array(out)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.4), gridspec_kw=dict(wspace=0.34))

# ---------------- 左：弯曲速度场上的 Euler 折线 ----------------
w = np.pi / 2
ax = axes[0]
tt = np.linspace(0, 1, 300)
ax.plot(np.cos(w * tt), np.sin(w * tt), color=INK, lw=1.4)
for n, col, lab in ((6, RED, "$N=6$"), (18, BLUE, "$N=18$")):
    p = euler_path(n, w)
    ax.plot(p[:, 0], p[:, 1], color=col, lw=0.9, ls="--", marker="o", ms=2.2,
            mfc="white", mew=0.7, label="Euler " + lab)
ax.scatter([1.0], [0.0], s=24, c=INK, zorder=6)
ax.scatter([0.0], [1.0], s=24, c=INK, zorder=6)
ax.text(1.10, -0.06, "起点", fontsize=8.2)
ax.text(0.52, 1.24, "终点", fontsize=8.2)
ax.annotate("", xy=(np.cos(w * 0.62), np.sin(w * 0.62)),
            xytext=(np.cos(w * 0.42), np.sin(w * 0.42)),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8))
ax.text(0.50, 0.20, "精确解", fontsize=8.2, color=INK)
ax.legend(loc="lower left", fontsize=8.0, handlelength=1.9)
ax.set_xlim(-0.25, 1.45)
ax.set_ylim(-0.35, 1.42)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right", "left", "bottom"))

# ---------------- 右：误差随步数 ----------------
ax = axes[1]
ns = np.array([2, 4, 8, 16, 32, 64, 128, 256])
curves = ((np.pi / 2, RED, "Euler", r"$\omega=\pi/2$", "-o"),
          (np.pi / 2, RED, "Heun", r"$\omega=\pi/2$", ":s"),
          (np.pi / 32, BLUE, "Euler", r"$\omega=\pi/32$", "-o"))
for wv, col, kind, lab, fm in curves:
    f = euler_path if kind == "Euler" else heun_path
    err = np.array([np.linalg.norm(f(int(n), wv)[-1] - np.array([np.cos(wv), np.sin(wv)])) for n in ns])
    ax.loglog(ns, err, color=col, lw=1.3 if kind == "Euler" else 0.9, ls="-" if kind == "Euler" else ":",
              marker=fm[-1], ms=2.6, label=kind + "，" + lab)
ax.loglog(ns, 2.4 / ns, color=GRAY, lw=0.8, ls="--", label=r"参考 $\propto 1/N$")
ax.set_xlabel("每单位时间的步数 $N$")
ax.set_ylabel("终点误差")
ax.set_xlim(1.7, 300)
ax.set_ylim(1e-9, 3)
ax.legend(loc="lower left", fontsize=7.2, handlelength=1.9, labelspacing=0.3)
style(ax, grid=True, spines=("top", "right"))

save(fig, "fig01_euler", CH)
