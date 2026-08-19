# -*- coding: utf-8 -*-
"""Publish one unique article a day: human drafts first, then Gemini."""
import glob
import json
import os
import random
import re
import sys
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.dirname(__file__))

from daily_drafts import DRAFTS
from topic_bank import TOPICS
from build_blog import write_post

USED_TOPICS = os.path.join(os.path.dirname(__file__), "used_topics.json")


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


def recent_categories(n=3):
    cats = set()
    for name in sorted(existing_files(), reverse=True)[:n]:
        with open(os.path.join("posts", name), encoding="utf-8") as f:
            html = f.read()
        m = re.search(r'class="tag">([^<]+)', html)
        if m:
            cats.add(m.group(1).strip())
    return cats


def load_used_topics():
    if not os.path.exists(USED_TOPICS):
        return []
    try:
        with open(USED_TOPICS, encoding="utf-8") as f:
            data = json.load(f)
        return list(data.get("topics", []))
    except Exception:
        return []


def save_used_topic(topic):
    used = load_used_topics()
    if topic not in used:
        used.append(topic)
    with open(USED_TOPICS, "w", encoding="utf-8") as f:
        json.dump({"topics": used}, f, ensure_ascii=False, indent=2)


def pick_draft(published):
    unused = [d for d in DRAFTS if d["title"] not in published]
    if not unused:
        return None, 0
    recent = recent_categories()
    varied = [d for d in unused if d["category"] not in recent] or unused
    return random.choice(varied), len(unused) - 1


def pick_topic(published):
    used = set(load_used_topics())
    used.update(published)
    unused = [t for t in TOPICS if t not in used]
    if not unused:
        unused = [t for t in TOPICS if t not in published]
    return random.choice(unused) if unused else random.choice(TOPICS)


def publish(article, today):
    files = existing_files()
    article = dict(article)
    article["file"] = unique_filename(today)
    article["date"] = today
    article["related"] = random.sample(files, k=min(2, len(files))) if files else []
    write_post(article)
    return article


def main():
    today = datetime.date.today().isoformat()
    if glob.glob(f"posts/{today}-*.html"):
        print(f"An article for {today} already exists. Skipping extra publish.")
        return 0

    published = existing_titles()
    draft, left = pick_draft(published)
    if draft:
        article = publish(draft, today)
        print(f"Published draft: {article['file']} — {article['title']}")
        print(f"Human drafts remaining: {left}")
        return 0

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("No unused drafts and GEMINI_API_KEY is missing. Skipping today.")
        print("Add repo secret GEMINI_API_KEY to keep publishing automatically.")
        return 0

    from ai_generate import generate_article

    last_error = None
    for attempt in range(3):
        topic = pick_topic(published)
        try:
            generated = generate_article(topic, published, api_key)
            article = publish(generated, today)
            save_used_topic(topic)
            print(f"Published AI article via {generated.get('_model')}: {article['file']}")
            print(f"Title: {article['title']}")
            print(f"Topic seed: {topic}")
            return 0
        except Exception as exc:
            last_error = exc
            print(f"AI attempt {attempt + 1} failed: {exc}")

    print("Could not generate a good AI article today:", last_error)
    return 0


if __name__ == "__main__":
    sys.exit(main())
