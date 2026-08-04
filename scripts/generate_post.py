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
    <!-- Google Fonts & FontAwesome -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google AdSense Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7778135355055222" crossorigin="anonymous"></script>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --accent-purple: #7c3aed;
            --accent-blue: #2563eb;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border-light: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            background-image: radial-gradient(at 50% 0%, rgba(124, 58, 237, 0.05) 0px, transparent 50%);
            line-height: 1.8;
            padding-bottom: 60px;
        }}
        .navbar {{
            padding: 18px 8%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-size: 1.5rem;
            font-weight: 900;
            color: var(--accent-purple);
            text-decoration: none;
        }}
        .container {{
            max-width: 850px;
            margin: 40px auto;
            padding: 40px;
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        }}
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 50px;
            background: #e0f2fe;
            color: #0284c7;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }}
        h1 {{ font-size: 2.2rem; font-weight: 900; color: #0f172a; margin-bottom: 15px; line-height: 1.4; }}
        .meta {{ display: flex; gap: 20px; color: var(--text-muted); font-size: 0.9em; border-bottom: 1px solid var(--border-light); padding-bottom: 20px; margin-bottom: 30px; }}
        .ad-container {{
            margin: 30px 0;
            padding: 20px;
            background: #f8fafc;
            border: 1px dashed var(--border-light);
            border-radius: 12px;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
        }}
        .article-body p {{ font-size: 1.1rem; color: #334155; margin-bottom: 20px; }}
        .article-body h3 {{ font-size: 1.4rem; color: var(--accent-purple); margin: 30px 0 15px; }}
        .article-body ul {{ margin-right: 25px; margin-bottom: 25px; color: #334155; }}
        .article-body li {{ margin-bottom: 10px; }}
        .btn-back {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 24px;
            border-radius: 50px;
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: #fff;
            text-decoration: none;
            font-weight: 700;
            margin-top: 30px;
            transition: opacity 0.2s;
        }}
        .btn-back:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="../index.html" class="logo"><i class="fa-solid fa-brain"></i> الفكر الذكي</a>
        <a href="../index.html" style="color:var(--accent-purple); text-decoration:none; font-weight:700;"><i class="fa-solid fa-arrow-right"></i> الرئيسية</a>
    </nav>
    <div class="container">
        <span class="badge"><i class="fa-solid fa-tag"></i> مقال تقني يومي</span>
        <h1>{selected_topic}</h1>
        <div class="meta">
            <span><i class="fa-regular fa-calendar"></i> {today}</span>
            <span><i class="fa-regular fa-user"></i> محرر الذكاء الاصطناعي</span>
        </div>
        
        <div class="ad-container">
            <!-- موقع البودكاست -->
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-7778135355055222"
                 data-ad-slot="5093830951"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

        <div class="article-body">
            <p>مرحباً بكم في مدونة الفكر الذكي. يمثل موضوع <strong>{selected_topic}</strong> حجر الزاوية في تحسين كفاءة العمليات الرقمية وتطوير استراتيجيات التدوين المعاصرة.</p>
            
            <h3>أهمية هذا الاتجاه المستقبلي:</h3>
            <p>في عصر التحول الرقمي السريع، تعتمد الشركات والمدونات على أحدث حلول الأتمتة لضمان أرشفة فورية، تجربة متميزة للمستخدم، وتحقيق أعلى مستويات الأرباح من الإعلانات الرقمية.</p>
            
            <h3>أبرز التوصيات والاستراتيجيات:</h3>
            <ul>
                <li>تطبيق أفضل معايير تحسين محركات البحث SEO بشكل متواصل.</li>
                <li>استخدام تصميم متجاوب فائق السرعة يدعم كافة الشاشات والأجهزة.</li>
                <li>توفير محتوى حصري غني بالقيمة المضافة للقارئ والزائر.</li>
            </ul>
        </div>

        <div class="ad-container">
            <!-- موقع البودكاست -->
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-7778135355055222"
                 data-ad-slot="5093830951"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

        <a href="../index.html" class="btn-back"><i class="fa-solid fa-arrow-right"></i> العودة للرئيسية</a>
    </div>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"تم إنشاء المقال بستايل نهاري فاخر: {filename}")

if __name__ == "__main__":
    generate_article()
