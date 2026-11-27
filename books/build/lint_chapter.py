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
BANNED = ["值得注意的是", "不难发现", "众所周知", "显而易见", "综上所述", "总而言之",
          "总的来说", "赋能", "助力", "一站式", "深度剖析", "极大地", "显著地",
          "让我们", "想象一下", "本文将", "本节将", "下面我们"]


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

    # 引号：中文必须用“”，代码块、行内代码、HTML 属性里的引号不算
    plain = re.sub(r"`[^`\n]*`", "", body)
    plain = re.sub(r'="[^"\n]*"', "", plain)
    straight = re.findall(r'"([^"\n]*)"', plain)
    n_cjk = sum(1 for x in straight if re.search(r"[\u4e00-\u9fff]", x))
    if n_cjk:
        warns.append("中文用了直角引号 %d 处，应改为“”" % n_cjk)
    if plain.count("“") != plain.count("”"):
        errs.append("中文引号“”不成对")

    # 编辑口径残留：扩写时的待办句
    LEFT = re.compile(r"[^。\n]{0,20}(?:补上这一句|补一个[^。\n]{0,10}推导|再补两句|值得补一句|（待补）|\(待补\)|TODO)[^。\n]{0,10}。")
    for mm in LEFT.finditer(s):
        errs.append("编辑口径残留：%s" % mm.group(0).strip()[:40])

    # 禁用词（与 review_chapters.py 保持一致）
    for w in BANNED:
        if w in s:
            warns.append("禁用词：%s" % w)

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
