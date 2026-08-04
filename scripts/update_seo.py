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

    # 2. Update Index.html with list of posts
    posts = glob.glob("posts/*.html")
    posts_links_html = ""
    
    for post in sorted(posts, reverse=True):
        clean_post = post.replace("\\", "/")
        title = clean_post
        try:
            with open(post, "r", encoding="utf-8") as pf:
                content = pf.read()
                match = re.search(r"<title>(.*?)</title>", content)
                if match:
                    title = match.group(1)
        except Exception:
            pass
            
        posts_links_html += f"""
        <div class="post-card" style="background:#fff; border-right:4px solid #0056b3; padding:15px; margin-bottom:15px; border-radius:6px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="margin:0 0 10px 0;"><a href="{clean_post}" style="color:#0056b3; text-decoration:none;">{title}</a></h3>
            <p style="margin:0; font-size:0.9em; color:#666;">رابط المقال: <a href="{clean_post}">{clean_post}</a></p>
        </div>"""
        
    if not posts_links_html:
        posts_links_html = "<p>جاري توليد المقالات اليومية تلقائياً...</p>"

    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            index_content = f.read()
            
        pattern = r'(<div id="posts-list">)(.*?)(</div>)'
        new_index_content = re.sub(pattern, f'\\1{posts_links_html}\\3', index_content, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_index_content)
        print("تم تحديث الصفحة الرئيسية index.html بالمقالات الجديدة بنجاح!")

if __name__ == "__main__":
    update_sitemap_and_index()
