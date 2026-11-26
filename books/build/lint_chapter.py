#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""章稿快速自检：图片路径、图号、公式符号、代码围栏、标题层级、分册引用。

用法：
    python books/build/lint_chapter.py books/beginner/chapters/ch12.md
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOOK_NAMES = {"beginner": "入门篇", "advanced": "进阶篇", "editing": "深入篇"}


def lint(path):
    errs, warns = [], []
    s = open(path, encoding="utf-8").read()
    lines = s.split("\n")

    # 章号
    m = re.search(r"ch(\d+)\.md$", path)
    ch = int(m.group(1)) if m else None
    if not lines or not lines[0].startswith("# "):
        errs.append("第一行必须是章标题（# 标题）")

    # 图片
    for mm in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", s):
        rel = mm.group(1)
        if rel.startswith("http"):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), rel))
        if not os.path.exists(target):
            errs.append("图片不存在：%s" % rel)

    # 图号
    if ch:
        for a, b in re.findall(r"图 (\d+)\.(\d+)", s):
            if int(a) != ch:
                errs.append("图号 %s.%s 与章号 %d 不一致" % (a, b, ch))

    # 代码围栏
    if s.count("\n```") % 2 != 0:
        errs.append("代码围栏 ``` 数量为奇数")

    # 公式符号：去掉代码块与行内代码后，$ 数量应为偶数
    body = re.sub(r"```.*?```", "", s, flags=re.S)
    body = re.sub(r"`[^`]*`", "", body)
    if body.count("$") % 2 != 0:
        warns.append("$ 数量为奇数，可能有未闭合的公式")

    # 标题层级
    levels = [len(x.group(1)) for x in re.finditer(r"(?m)^(#{1,6}) ", s)]
    for i in range(1, len(levels)):
        if levels[i] > levels[i - 1] + 1:
            warns.append("标题层级跳跃：第 %d 个标题" % (i + 1))
            break

    # 分册引用
    book = os.path.basename(os.path.dirname(os.path.dirname(path)))
    own = BOOK_NAMES.get(book, "")
    for mm in re.finditer(r"(入门篇|进阶篇|深入篇)", s):
        if mm.group(1) != own:
            warns.append("出现其他分册名：%s" % mm.group(1))

    chars = len(re.findall(r"[\u4e00-\u9fa5]", s))
    return chars, errs, warns


def main():
    if len(sys.argv) < 2:
        print("用法: python books/build/lint_chapter.py <章文件> [...]")
        return
    bad = 0
    for p in sys.argv[1:]:
        chars, errs, warns = lint(p)
        name = os.path.basename(p)
        status = "OK " if not errs else "ERR"
        print("%s %-12s %5d 汉字" % (status, name, chars))
        for e in errs:
            print("    [错误]", e)
        for w in warns:
            print("    [提醒]", w)
        bad += len(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
