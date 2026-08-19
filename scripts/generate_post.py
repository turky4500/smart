# -*- coding: utf-8 -*-
"""Publish one unused unique draft each day. Never repeats a title."""
import glob
import os
import random
import re
import sys
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.dirname(__file__))

from daily_drafts import DRAFTS
from build_blog import write_post


def existing_titles():
    titles = set()
    for path in glob.glob("posts/*.html"):
        with open(path, encoding="utf-8") as f:
            html = f.read()
        m = re.search(r"<h1>(.*?)</h1>", html, re.S)
        if m:
            titles.add(re.sub(r"\s+", " ", m.group(1)).strip())
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if m:
            titles.add(re.sub(r"\s+\|.*$", "", re.sub(r"\s+", " ", m.group(1))).strip())
    return titles


def existing_files():
    return [os.path.basename(p) for p in glob.glob("posts/*.html")]


def unique_filename(today):
    used = set(existing_files())
    for _ in range(50):
        name = f"{today}-{random.randint(100, 999)}.html"
        if name not in used:
            return name
    raise RuntimeError("could not allocate a unique filename")


def main():
    today = datetime.date.today().isoformat()
    if glob.glob(f"posts/{today}-*.html"):
        print(f"An article for {today} already exists. Skipping extra publish.")
        return 0

    published = existing_titles()
    unused = [d for d in DRAFTS if d["title"] not in published]
    if not unused:
        print("No unused drafts left. Skipping to protect uniqueness.")
        return 0

    # Prefer a category not used in the last 3 posts for variety.
    recent = sorted(existing_files(), reverse=True)[:3]
    recent_cats = set()
    for name in recent:
        with open(os.path.join("posts", name), encoding="utf-8") as f:
            html = f.read()
        m = re.search(r'class="tag">([^<]+)', html)
        if m:
            recent_cats.add(m.group(1).strip())
    varied = [d for d in unused if d["category"] not in recent_cats] or unused
    draft = random.choice(varied)

    files = existing_files()
    related = random.sample(files, k=min(2, len(files))) if files else []

    article = dict(draft)
    article["file"] = unique_filename(today)
    article["date"] = today
    article["related"] = related

    write_post(article)
    left = len(unused) - 1
    print(f"Published: {article['file']} — {article['title']}")
    print(f"Unused drafts remaining: {left}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
