import os
import glob
import datetime

def update_sitemap():
    domain = "https://turky4500.github.io/smart"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # تجميع كافة صفحات ومشروعات المستودع (a.html, soq.html, posts/*.html, إلخ)
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

if __name__ == "__main__":
    update_sitemap()
