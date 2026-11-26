#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扩写后的整册体检：字数分布、重复段落、禁用词、跨册词、标题重复。"""
import glob
import os
import re
import sys
from collections import Counter

BANNED = ["值得注意的是", "不难发现", "众所周知", "显而易见", "综上所述", "总而言之",
          "总的来说", "赋能", "助力", "一站式", "深度剖析", "极大地", "显著地",
          "让我们", "想象一下", "本文将", "本节将", "下面我们"]
BOOKS = {"beginner": "入门篇", "advanced": "进阶篇", "editing": "深入篇"}


def main(book):
    files = sorted(glob.glob("books/%s/chapters/ch*.md" % book))
    total = 0
    print("== %s" % BOOKS.get(book, book))
    for f in files:
        s = open(f, encoding="utf-8").read()
        n = len(re.findall(r"[\u4e00-\u9fa5]", s))
        total += n
        flags = []
        heads = re.findall(r"(?m)^#{2,3} (.+)$", s)
        dup = [h for h, c in Counter(heads).items() if c > 1]
        if dup:
            flags.append("重复标题 %s" % dup[:2])
        paras = [p.strip() for p in re.split(r"\n\s*\n", s) if len(p.strip()) > 80]
        pc = Counter(paras)
        rep = [p[:24] for p, c in pc.items() if c > 1]
        if rep:
            flags.append("重复段落 %d 处，如「%s」" % (len(rep), rep[0]))
        bad = [w for w in BANNED if w in s]
        if bad:
            flags.append("禁用词 %s" % bad)
        other = [v for k, v in BOOKS.items() if k != book and v in s]
        if other:
            flags.append("跨册词 %s" % other)
        print("  %-12s %5d  %s" % (os.path.basename(f), n, "；".join(flags)))
    print("  合计 %d 汉字，%d 章，平均 %d" % (total, len(files), total / max(1, len(files))))


if __name__ == "__main__":
    for b in (sys.argv[1:] or ["beginner", "advanced", "editing"]):
        main(b)
