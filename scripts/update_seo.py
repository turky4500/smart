# -*- coding: utf-8 -*-
"""Refresh sitemap and homepage cards from unique posts only."""
import os
import re
import glob
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://turky4500.github.io/smart"

BLOG_PAGES = [
    ("index.html", "1.0"),
    ("about.html", "0.6"),
    ("contact.html", "0.5"),
    ("privacy.html", "0.5"),
    ("disclaimer.html", "0.4"),
]

MONTHS = {
    1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
    7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر",
}


def arabic_date(iso):
    try:
        y, m, d = [int(x) for x in iso.split("-")]
        return f"{d} {MONTHS[m]} {y}"
    except Exception:
        return iso


def post_meta(path):
    name = os.path.basename(path)
    date = name[:10] if re.match(r"\d{4}-\d{2}-\d{2}", name) else datetime.date.today().isoformat()
    title = name
    category = "مقال"
    excerpt = ""
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).replace("| مدونة الفكر الذكي", "").replace("- مدونة الفكر الذكي", "").strip()
    m = re.search(r'class="tag">([^<]+)', html)
    if m:
        category = m.group(1).strip()
    m = re.search(r'class="summary">([^<]+)', html)
    if m:
        excerpt = m.group(1).strip()
    return {
        "file": "posts/" + name,
        "date": date,
        "title": title,
        "category": category,
        "excerpt": excerpt,
    }


def update_sitemap(posts):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri in BLOG_PAGES:
        loc = f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"
        full = os.path.join(ROOT, path)
        if os.path.exists(full):
            last = datetime.date.fromtimestamp(os.path.getmtime(full)).isoformat()
            lines.append(f"  <url><loc>{loc}</loc><lastmod>{last}</lastmod><priority>{pri}</priority></url>")
    for p in posts:
        lines.append(
            f"  <url><loc>{SITE}/{p['file']}</loc><lastmod>{p['date']}</lastmod><priority>0.8</priority></url>"
        )
    lines.append("</urlset>\n")
    path = os.path.join(ROOT, "sitemap.xml")
    content = "\n".join(lines)
    if os.path.exists(path) and open(path, encoding="utf-8").read() == content:
        print("sitemap unchanged")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("sitemap updated:", len(posts), "posts")


def card_html(p):
    excerpt = p["excerpt"] or p["title"]
    return f"""
        <article class="card" data-category="{p['category']}">
          <div class="card-top"><i class="fa-solid fa-lightbulb"></i></div>
          <div class="card-body">
            <span class="tag">{p['category']}</span>
            <h3><a href="{p['file']}">{p['title']}</a></h3>
            <p class="excerpt">{excerpt}</p>
            <div class="card-meta">
              <span>{arabic_date(p['date'])}</span>
              <a href="{p['file']}">اقرأ المقال</a>
            </div>
          </div>
        </article>"""


def update_index(posts):
    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, encoding="utf-8") as f:
        html = f.read()
    cards = "".join(card_html(p) for p in posts)
    pattern = r"<!-- POSTS_START -->.*?<!-- POSTS_END -->"
    if not re.search(pattern, html, re.S):
        print("WARNING: POSTS markers missing in index.html — left unchanged")
        return
    html = re.sub(
        pattern,
        f"<!-- POSTS_START -->\n      {cards}\n      <!-- POSTS_END -->",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"\d+ مقالًا أصليًا",
        f"{len(posts)} مقالًا أصليًا",
        html,
        count=1,
    )
    cats = ["الكل"] + sorted({p["category"] for p in posts if p["category"]})
    filters = []
    for i, c in enumerate(cats):
        cls = "filter-btn active" if i == 0 else "filter-btn"
        filters.append(f'<button class="{cls}" type="button" data-filter="{c}">{c}</button>')
    html = re.sub(
        r'<div class="filters">.*?</div>',
        f'<div class="filters">{"".join(filters)}</div>',
        html,
        count=1,
        flags=re.S,
    )
    if os.path.exists(index_path) and open(index_path, encoding="utf-8").read() == html:
        print("index unchanged")
        return
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index cards updated")


def main():
    os.chdir(ROOT)
    files = sorted(glob.glob("posts/*.html"), reverse=True)
    posts = [post_meta(p) for p in files]
    posts.sort(key=lambda x: x["date"], reverse=True)
    update_sitemap(posts)
    update_index(posts)


if __name__ == "__main__":
    main()
