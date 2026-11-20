"""生成封面与封底：铺满 + 居中裁切的背景图，压暗后放标题。

用法：
    python books/code/common/make_cover.py --book books/beginner --front logo4.png --back logo12.png
"""
import argparse
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGOS = r"E:\Study\0-logo"
W, H = 1760, 2500  # 176×250 mm @ 254 dpi


def make(src, dst, dark=0.32, bottom=0.72):
    im = Image.open(src).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale + 1), int(im.height * scale + 1)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))

    alpha = Image.new("L", (1, H))
    for y in range(H):
        v = int(255 * (dark + (bottom - dark) * y / H))
        alpha.putpixel((0, y), v)
    alpha = alpha.resize((W, H))
    black = Image.new("RGBA", (W, H), (6, 10, 20, 255))
    black.putalpha(alpha)
    im = Image.alpha_composite(im.convert("RGBA"), black).convert("RGB")
    im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
    print("wrote", os.path.relpath(dst, ROOT), "%.0f KB" % (os.path.getsize(dst) / 1024))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="books/beginner")
    ap.add_argument("--front", default="logo4.png")
    ap.add_argument("--back", default="logo12.png")
    ap.add_argument("--dark", type=float, default=0.32)
    ap.add_argument("--bottom", type=float, default=0.72)
    ap.add_argument("--back-dark", type=float, default=0.55)
    args = ap.parse_args()

    out = os.path.join(ROOT, args.book, "images")
    os.makedirs(out, exist_ok=True)
    make(os.path.join(LOGOS, args.front), os.path.join(out, "cover.jpg"), args.dark, args.bottom)
    make(os.path.join(LOGOS, args.back), os.path.join(out, "backcover.jpg"), args.back_dark, 0.9)
