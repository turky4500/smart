import os
import datetime
import random

def generate_article():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    topics = [
        "أهم استراتيجيات الذكاء الاصطناعي لتطوير الأعمال في 2026",
        "كيف تحسن من سرعة موقعك الإلكتروني لزيادة تحويلات AdSense",
        "أفضل أدوات التدوين الرقمي لزيادة عدد الزوار وتصدر نتائج قوقل",
        "مستقبل الحوسبة السحابية والأمن السيبراني للمبتدئين",
        "طرق تحسين تجربة المستخدم SEO ودورها في زيادة الأرباح"
    ]
    
    selected_topic = random.choice(topics)
    filename = f"posts/{today}-{random.randint(100,999)}.html"
    os.makedirs("posts", exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{selected_topic} - مدونة الفكر الذكي</title>
    <meta name="description" content="اقرأ مقالنا اليومي حول {selected_topic} وأحدث النصائح التقنية لتحسين موقعك والأرشفة في قوقل.">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_PUBLISHER_ID" crossorigin="anonymous"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.8; margin: 0; padding: 20px; background: #f9f9f9; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        h1, h2 {{ color: #0056b3; }}
        .meta {{ font-size: 0.9em; color: #666; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .ad-slot {{ background: #f0f0f0; border: 1px dashed #ccc; padding: 15px; text-align: center; margin: 20px 0; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1><a href="../index.html" style="text-decoration:none; color:#0056b3;">مدونة الفكر الذكي</a></h1>
        <hr>
        <article>
            <h2>{selected_topic}</h2>
            <div class="meta">تاريخ النشر: {today} | بقلم: محرر الذكاء الاصطناعي</div>
            
            <div class="ad-slot">
                <!-- مكان إعلان AdSense العلوي -->
            </div>

            <p>مرحباً بكم في مقالنا اليومي المحدث تلقائياً. يمثل <strong>{selected_topic}</strong> أحد أهم المحاور التي تشغل بال المتخصصين في مجال التقنية والتسويق الرقمي اليوم.</p>
            
            <h3>أبرز النقاط المستفادة:</h3>
            <ul>
                <li>تحسين الأداء وسرعة التحميل.</li>
                <li>توفير تصميم متجاوب مع جميع الأجهزة.</li>
                <li>الأرشفة الفورية عبر محركات البحث.</li>
            </ul>

            <div class="ad-slot">
                <!-- مكان إعلان AdSense السفلي -->
            </div>
            
            <p><small>آخر تحديث: {timestamp}</small></p>
        </article>
        <hr>
        <p><a href="../index.html">العودة للصفحة الرئيسية</a></p>
    </div>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"تم إنشاء المقال: {filename}")

if __name__ == "__main__":
    generate_article()
