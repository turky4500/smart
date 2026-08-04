import os
import glob
import datetime
import re

def update_sitemap_and_index():
    domain = "https://turky4500.github.io/smart"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 1. Update Sitemap
    all_html_files = glob.glob("*.html") + glob.glob("posts/*.html")
    urls = []
    for file_path in set(all_html_files):
        clean_path = file_path.replace("\\", "/")
        priority = "1.0" if clean_path == "index.html" else "0.8"
        urls.append(f"  <url>\n    <loc>{domain}/{clean_path}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>")
    
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{'\n'.join(urls)}
</urlset>"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("تم أرشفة وتجميع كافة المشروعات والصفحات في sitemap.xml بنجاح!")

    # 2. Update Index.html with beautiful post cards
    posts = glob.glob("posts/*.html")
    posts_cards_html = ""
    
    icons = [
        "fa-solid fa-lightbulb",
        "fa-solid fa-chart-line",
        "fa-solid fa-laptop-code",
        "fa-solid fa-newspaper",
        "fa-solid fa-rocket"
    ]
    
    tags = ["استراتيجيات وتطوير", "SEO وتصنيف", "تسويق رقمي", "تقنية مستقبليات", "تنمية أرباح"]

    for idx, post in enumerate(sorted(posts, reverse=True)):
        clean_post = post.replace("\\", "/")
        title = clean_post
        try:
            with open(post, "r", encoding="utf-8") as pf:
                content = pf.read()
                match = re.search(r"<title>(.*?)</title>", content)
                if match:
                    title = match.group(1).replace("- مدونة الفكر الذكي", "").strip()
        except Exception:
            pass
            
        icon = icons[idx % len(icons)]
        tag = tags[idx % len(tags)]
        
        posts_cards_html += f"""
        <article class="post-card">
            <div class="card-header-icon">
                <i class="{icon}"></i>
            </div>
            <div class="card-body">
                <span class="card-tag">{tag}</span>
                <a href="{clean_post}" class="card-title">{title}</a>
                <div class="card-footer">
                    <span><i class="fa-regular fa-calendar"></i> {today}</span>
                    <a href="{clean_post}" class="btn-read">اقرأ المقال <i class="fa-solid fa-arrow-left"></i></a>
                </div>
            </div>
        </article>"""
        
    if not posts_cards_html:
        posts_cards_html = '<p style="color:var(--text-muted); text-align:center;">جاري نشر المقالات اليومية...</p>'

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            index_content = f.read()
            
        pattern = r'(<div id="posts-list"[^>]*>)(.*?)(</div>)'
        new_index_content = re.sub(pattern, f'\\1{posts_cards_html}\n        \\3', index_content, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_index_content)
        print("تم تحديث بطاقات المقالات في الصفحة الرئيسية index.html بنجاح!")

if __name__ == "__main__":
    update_sitemap_and_index()
