import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "12"

# ---------- 图 12.2 时间一致性的定量度量 ----------
rng = np.random.default_rng(7)
H = W = 80
SQ = 24
DX = 2

yy, xx = np.mgrid[0:H, 0:W]
bg = 0.55 + 0.10 * (yy / float(H)) + 0.02 * np.sin(xx / 9.0)

_g = np.arange(SQ)
tex = 0.5 + 0.25 * np.sin(_g[None, :] / 2.7) * np.cos(_g[:, None] / 3.1)
tex = np.clip(tex + 0.10 * np.random.default_rng(11).normal(0, 1, (SQ, SQ)), 0, 1)


def make_frame(t, jitter_sigma):
    img = bg.copy()
    x0 = 6 + DX * t
    img[26:26 + SQ, x0:x0 + SQ] = tex
    img = img + rng.normal(0, jitter_sigma, img.shape) + rng.normal(0, jitter_sigma * 0.6)
    return np.clip(img, 0, 1)


NFR = 12
seq = {
    "帧间细节共享": [make_frame(t, 0.0015) for t in range(NFR + 1)],
    "逐帧独立生成": [make_frame(t, 0.010) for t in range(NFR + 1)],
}

inner = (slice(4, H - 4), slice(6, W - 4))


def warp_known(a, t):
    # 已知位移的运动补偿：物体区域右移 DX，背景不动
    out = a.copy()
    x0 = 6 + DX * t
    out[26:26 + SQ, x0 + DX:x0 + DX + SQ] = a[26:26 + SQ, x0:x0 + SQ]
    return out


def warp_err(a, b, t):
    aligned = warp_known(a, t)
    return float(np.mean(np.abs(b[inner] - aligned[inner])) * 255)


errs = {k: [warp_err(v[t], v[t + 1], t) for t in range(NFR)] for k, v in seq.items()}

fig = plt.figure(figsize=(W_FULL, 2.75))
outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.25], hspace=0.62)
top = outer[0].subgridspec(1, 3, wspace=0.14)

t0 = 4
res_map = np.abs(seq["逐帧独立生成"][t0 + 1] - warp_known(seq["逐帧独立生成"][t0], t0))
panels = [
    (seq["帧间细节共享"][t0], "帧 $t$", 1.0),
    (seq["逐帧独立生成"][t0 + 1], "帧 $t+1$（独立生成）", 1.0),
    (res_map, "扭曲后的残差", 0.014),
]
for k, (img, lab, vmax) in enumerate(panels):
    ax = fig.add_subplot(top[0, k])
    ax.imshow(img, cmap="gray", vmin=0, vmax=vmax, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#8a8a8a")
        sp.set_linewidth(0.5)
    ax.set_xlabel(lab, fontsize=7.0, labelpad=2.5, color=INK)

ax = fig.add_subplot(outer[1])
xs = np.arange(1, NFR + 1)
ax.plot(xs, errs["逐帧独立生成"], color=RED, lw=1.4, marker="o", ms=2.8, label="逐帧独立生成")
ax.plot(xs, errs["帧间细节共享"], color=BLUE, lw=1.4, marker="o", ms=2.8, label="帧间细节共享")
ax.set_xlabel("帧对 $t\\to t+1$")
ax.set_ylabel("扭曲残差（灰阶）")
ax.set_ylim(0, max(errs["逐帧独立生成"]) * 1.35)
ax.set_xlim(0, NFR + 1)
ax.set_xticks([1, 4, 8, 12])
ax.legend(loc="upper right", fontsize=7.2, ncol=2)
style(ax, grid=True)
save(fig, "fig12_consistency", CH)

# ---------- 图 12.3 注意力随时长的规模 ----------
Tp = np.arange(1, 41)
NL = 4096
full = (NL * Tp) ** 2
fact = NL ** 2 * Tp + Tp ** 2 * NL
conv = 81 * NL * Tp

fig, ax = plt.subplots(figsize=(W_FULL * 0.92, 2.45))
ax.loglog(Tp, full, color=RED, lw=1.6)
ax.loglog(Tp, fact, color=BLUE, lw=1.6)
ax.loglog(Tp, conv, color=GREEN, lw=1.4, ls=(0, (4, 2)))

ax.axhline(1e9, color=GRAY, lw=0.8, ls=(0, (1, 3)))
ax.text(1.2, 1.25e9, "fp16 下约 2 GB", fontsize=7.2, color=GRAY, va="bottom")

ax.set_xlim(1, 92)
ax.set_xscale("log")
ax.set_ylim(2e6, 1e13)
ax.set_xticks([1, 2, 4, 8, 16, 40])
ax.set_xticklabels(["1", "2", "4", "8", "16", "40"])
ax.set_xlabel("潜空间帧数 $T$（空间 token 数 $N=4096$）")
ax.set_ylabel("注意力矩阵元素数")
style(ax, grid=True)

for yv, txt, c in [(full[-1], "全 3D 注意力", RED),
                   (fact[-1], "时空分解", BLUE),
                   (conv[-1] * 3, "只用卷积", GREEN)]:
    ax.text(43, yv, txt, fontsize=7.4, color=c, va="center")
save(fig, "fig12_budget", CH)
