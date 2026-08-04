import os
import datetime
import random

ARTICLES_DATABASE = [
    {
        "title": "دليل شامل: كيف تحسن من سرعة موقعك الإلكتروني لزيادة أرباح AdSense ومعدل التحويل",
        "category": "تحسين الأداء وSEO",
        "author": "م. أحمد سليمان - خبير البنية التحتية والسيو",
        "summary": "استكشف في هذا المقال العملي أفضل الاستراتيجيات والتقنيات المتقدمة لتسريع موقعك الإلكتروني، وتقليل وقت استجابة السيرفر، ومضاعفة أرباح إعلاناتك عبر تحسين تجربة المستخدم.",
        "sections": [
            {
                "heading": "أهمية سرعة الموقع في معادلة أرباح أدسينس وترتيب محركات البحث",
                "content": "تعتبر سرعة تحميل الموقع الإلكتروني أحد أهم العوامل الرئيسية التي تعتمد عليها خوارزميات قوقل (Core Web Vitals) لتحديد ترتيب موقعك في نتائج البحث الأولى. تشير الدراسات إلى أن تأخر تحميل الصفحة لمدة ثانية واحدة فقط قد يؤدي إلى خسارة أكثر من 10% من الزوار، وبالتالي انخفاض مباشر في نقرات الإعلانات وعائد الأرباح (RPM)."
            },
            {
                "heading": "1. ضغط الصور واختيار الصيغ الحديثة (WebP & AVIF)",
                "content": "تمثل الصور عادة أكثر من 60% من حجم الصفحة الكلي. للحصول على سرعة فائقة، يجب تحويل كافة الصور إلى صيغ حديثة مثل WebP أو AVIF، وضغطها دون التأثير على الجودة بصرياً. كما يُوصى بشدة باستخدام ميزة التحميل الكسول (Lazy Loading) لعدم تحميل الصور إلا عند وصول الزائر إليها أثناء التمرير."
            },
            {
                "heading": "2. الاستفادة من شبكات توزيع المحتوى (CDN) والتخزين المؤقت",
                "content": "تتيح لك شبكات توزيع المحتوى مثل Cloudflare تقديم صفحات موقعك من أقرب سيرفر جغرافي للزائر، مما يقلل زمن التردد (Latency) بشكل هائل. قم أيضاً بتفعيل التخزين المؤقت للمتصفح (Browser Caching) وتقليل طلبات HTTP المباشرة للسيرفر الرئيسي."
            },
            {
                "heading": "3. ضغط وتحسين أكواد CSS و JavaScript",
                "content": "الأكواد البرمجية الزائدة تؤدي إلى إبطاء عملية رندر الصفحة (Render-Blocking Resources). قم بتجميع وضغظ ملفات السكريبت والأنماط، وتأجيل تحميل أكواد الإعلانات والتحليلات لتعمل بشكل غير متزامن (Asynchronous Loading) حتى لا تعطل ظهور المحتوى الأساسي للزائر."
            }
        ],
        "key_takeaways": [
            "سرعة التحميل تحت 2 ثانية ترفع معدل البقاء في الموقع بنسبة 40%.",
            "استخدام صيغ WebP يوفر أكثر من 50% من حجم البيانات.",
            "التأجيل الذكي لأكواد الإعلانات يزيد من نسبة الظهور الفعلي (Viewability Rate)."
        ]
    },
    {
        "title": "أفضل استراتيجيات التسويق الرقمي وتنمية حركة الزوار (Traffic) للمدونات التقنية",
        "category": "التسويق الرقمي والنمو",
        "author": "د. سارة خالد - مستشارة التسويق بالمحتوى",
        "summary": "تعرف على الأساليب الحديثة لجذب آلاف الزوار المهتمين لموقعك يومياً، وكيفية بناء سلطة رقمية (Domain Authority) تجعل موقعك المقصد الأول في مجالك.",
        "sections": [
            {
                "heading": "مفهوم بناء السلطة الرقمية (Digital Authority)",
                "content": "في عالم النشر الحديث، لا يكفي فقط نشر المقالات، بل يجب تقديم رؤية عميقة وتحليلات ذات قيمة مضافة عالية تجعل القارئ ينظر لموقعك كمرجع موثوق. هذا النهج يضمن زيادة معدل العودة للموقع (Returning Visitors) وبناء قاعدة جماهيرية وفية."
            },
            {
                "heading": "استهداف الكلمات المفتاحية ذات القصد الشرائي (Search Intent)",
                "content": "بدلاً من استهداف كلمات عامة ومنافسة بشدة، ركز على الكلمات المفتاحية الطويلة (Long-tail Keywords) التي تبحث عن حلول لمشاكل محددة. هذه الكلمات تتميز بمعدل تحويل مرتفع وتجذب زواراً مستعدين للتفاعل مع المحتوى والإعلانات."
            },
            {
                "heading": "تطوير استراتيجية المحتوى الشامل (Pillar Pages & Content Clusters)",
                "content": "قم بإنشاء دليل رئيسي شامل للموضوع، ثم اربطه بمقالات فرعية مفصلة تغطي كافة الجوانب ذات الصلة. هذا الهيكل التنظيمي يساعد محركات البحث على فهم شمولية موقعك ويسمح للزائر بالانتقال السلس بين صفحاتك."
            }
        ],
        "key_takeaways": [
            "التركيز على نية الباحث (Search Intent) أهم من كثافة الكلمات المفتاحية.",
            "الربط الداخلي المحسب الذكي يقلل معدل الارتداد (Bounce Rate).",
            "تقديم إجابات مباشرة ودقيقة يضمن الظهور في الإجابات المباشرة لقوقل (Featured Snippets)."
        ]
    },
    {
        "title": "دليل بناء سلطة المورد الرقمي (Domain Authority) وتصدر نتائج محركات البحث SEO",
        "category": "استراتيجيات SEO",
        "author": "م. خالد منصور - خبير تحسين محركات البحث",
        "summary": "خطوات عملية وواضحة لتحسين ترتيب موقعك في محرك البحث قوقل وبناء الروابط الخلفية عالية الجودة بطرق شرعية وآمنة.",
        "sections": [
            {
                "heading": "ما هو الـ Domain Authority وكيف تؤثر خوارزميات قوقل عليه؟",
                "content": "يُعبر الدومين أثوريتي عن جودة ومدى ثقة محركات البحث في موقعك مقارنة بآلاف المواقع المنافسة. يبنى هذا المؤشر عبر تضافر عوامل متعددة تشمل قدم النطاق، جودة المحتوى، وهيكلية الموقع البرمجية السليمة."
            },
            {
                "heading": "استراتيجية الروابط الخلفية الخارجية (Backlinks) الطبيعية",
                "content": "الروابط الخارجية القادمة من مواقع ذات موثوقية عالية تعمل كشهادة تزكية لموقعك لدى محركات البحث. تجنب شراء الروابط العشوائية أو السبام، وركز على نشر أبحاث ومقالات مميزة تجعل المواقع العالمية تشير إليك كمصدر رسمي."
            },
            {
                "heading": "تحسين تجربة المستخدم الهيكلية (Technical SEO)",
                "content": "تأكد من خلو موقعك من أخطاء الروابط المكسورة (404 Error)، وتوفير شهادة الأمان SSL (HTTPS)، وضمان توافق كافة الصفحات مع الهواتف الذكية بنسبة 100%."
            }
        ],
        "key_takeaways": [
            "الروابط الخلفية القوية تزيد من سرعة أرشفة الصفحات الجديدة.",
            "استخدام شهادة SSL وحماية البيانات هو شرط أساسي للترتيب في الصفحة الأولى.",
            "الهيكلية الواضحة لملف sitemap تفهرس كل مقال خلال ساعات قليلة."
        ]
    },
    {
        "title": "كيفية اختيار واستغلال الكلمات المفتاحية ذات الربحية العالية (High CPC Keywords)",
        "category": "تحقيق الدخل وAdSense",
        "author": "أ. طارق عبدالكريم - متخصص أرباح الإعلانات",
        "summary": "تعلم كيفية العثور على الكلمات المفتاحية التي يدفع المعنون مبالغ مرتفعة لقاء الإعلان عليها ومضاعفة عائد ألف ظهور (RPM) في موقعك.",
        "sections": [
            {
                "heading": "فهم آلية المزادات في Google AdSense وكيفية حساب سعر النقرة",
                "content": "تعتمد أرباح الإعلانات على نظام المزاد المباشر بين المعلنين. القطاعات التقنية والمالية والاستثمارية والتأمين تشهد منافسة شديدة تجعل سعر النقرة الواحدة يتضاعف مرات عديدة مقارنة بالقطاعات العامة."
            },
            {
                "heading": "أدوات البحث عن الكلمات المفتاحية الربحية",
                "content": "استخدم أدوات مثل Google Keyword Planner و Ahrefs للتعرف على تكلفة النقرة المتوقعة (CPC) وحجم البحث الشهري. قم باستهداف المواضيع ذات القيمة التجارية العالية لتغطيتها بمقالات دقيقة."
            },
            {
                "heading": "التوزيع الذكي للإعلانات بداخل المقال لتحقيق أعلى معدل مشاهدة (Viewability)",
                "content": "قم بوضع الإعلانات في أماكن انتباه القارئ الطبيعية، مثل أعلى المقال وتحت الفقرات الرئيسية. تجنب تكثيف الإعلانات بشكل يزعج الزائر، بل حافظ على توازن رائع بين تجربة القراءة وتصميم الإعلان."
            }
        ],
        "key_takeaways": [
            "استهداف النيش (Niche) التخصصي يرفع سعر النقرة بنسبة تصل إلى 300%.",
            "التوزيع الجيد للإعلان يمنع النقرات الخاطئة ويحافظ على حساب AdSense سليم.",
            "متابعة تحليلات AdSense الدورية تمكنك من معرفة أفضل المقالات أرباحاً وتكرار تجربتها."
        ]
    },
    {
        "title": "دليل تصميم وتجربة المستخدم UX/UI لزيادة وقت بقاء الزائر ومعدل التفاعل",
        "category": "تصميم وتجربة المستخدم",
        "author": "أ. مريم يوسف - مصممة واجهات رقمية",
        "summary": "شرح عملي لأهم مبادئ واجهة وتجربة المستخدم وكيفية تحويل مدونتك إلى منصة جذابة تشجع الزوار على الاستمرار والاستكشاف.",
        "sections": [
            {
                "heading": "أهمية التناسق البصري وقراءة الخطوط على الشاشات المختلفة",
                "content": "التصميم الأنيق البسيط يعتمد على خطوط واضحة مثل Cairo وبحجم مريح للعاطفة، مع مسافات فاصلة بين الأسطر (Line Height). التناسق بين الألوان الداكنة والفاتحة يعطي شعوراً بالفخامة والاحترافية."
            },
            {
                "heading": "تصميم بطاقات المقالات (Article Cards) الجذابة",
                "content": "البطاقات المنسقة ذات الحدود الناعمة والوسوم الملونة تزيد من نسبة الضغط على المقالات (CTR) بشكل ملحوظ مقارنة بالقوائم النصية التقليدية البحتة."
            },
            {
                "heading": "التنقل السلس والوصول المباشر للمحتوى ذات الصلة",
                "content": "وفر دائماً أزرار العودة للرئيسية وروابط المقالات المتصلة في نهاية كل مقال لتمكين القارئ من التنقل بحرية دون مغادرة موقعك."
            }
        ],
        "key_takeaways": [
            "زيادة وقت بقاء الزائر ترفع تقييم موقعك في خوارزميات محركات البحث.",
            "التصميم النظيف الاستجابي يضمن عمل الموقع بكفاءة على شاشات الأبل والأندرويد.",
            "الألوان المتناسقة المريحة للعين تقلل معدل مغادرة الصفحة السريعة."
        ]
    }
]

def generate_article(target_file=None):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    article_data = random.choice(ARTICLES_DATABASE)
    title = article_data["title"]
    category = article_data["category"]
    author = article_data["author"]
    summary = article_data["summary"]
    sections = article_data["sections"]
    takeaways = article_data["key_takeaways"]
    
    if not target_file:
        filename = f"posts/{today}-{random.randint(100,999)}.html"
    else:
        filename = target_file
        
    os.makedirs("posts", exist_ok=True)
    
    sections_html = ""
    for sec in sections:
        sections_html += f"""
        <section class="content-section">
            <h3>{sec['heading']}</h3>
            <p>{sec['content']}</p>
        </section>"""
        
    takeaways_html = "".join([f"<li><i class='fa-solid fa-check-circle' style='color:#7c3aed; margin-left:8px;'></i> {item}</li>" for item in takeaways])
    
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - مدونة الفكر الذكي</title>
    <meta name="description" content="{summary}">
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
            line-height: 1.9;
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
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .logo {{
            font-size: 1.5rem;
            font-weight: 900;
            color: var(--accent-purple);
            text-decoration: none;
        }}
        .container {{
            max-width: 900px;
            margin: 40px auto;
            padding: 45px;
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        }}
        .category-badge {{
            display: inline-block;
            padding: 6px 18px;
            border-radius: 50px;
            background: #e0f2fe;
            color: #0284c7;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 20px;
        }}
        h1 {{ font-size: 2.3rem; font-weight: 900; color: #0f172a; margin-bottom: 20px; line-height: 1.4; }}
        .meta {{ display: flex; flex-wrap: wrap; gap: 25px; color: var(--text-muted); font-size: 0.9em; border-bottom: 1px solid var(--border-light); padding-bottom: 20px; margin-bottom: 35px; }}
        .summary-box {{
            background: #f1f5f9;
            border-right: 4px solid var(--accent-purple);
            padding: 20px 25px;
            border-radius: 12px;
            font-size: 1.15rem;
            color: #334155;
            margin-bottom: 35px;
            font-weight: 600;
        }}
        .ad-container {{
            margin: 35px 0;
            padding: 15px;
            background: #f8fafc;
            border: 1px dashed var(--border-light);
            border-radius: 14px;
            text-align: center;
        }}
        .content-section {{ margin-bottom: 35px; }}
        .content-section h3 {{ font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; }}
        .content-section p {{ font-size: 1.1rem; color: #334155; margin-bottom: 15px; }}
        .takeaways-card {{
            background: rgba(124, 58, 237, 0.04);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-radius: 18px;
            padding: 25px 30px;
            margin: 40px 0;
        }}
        .takeaways-card h4 {{ font-size: 1.25rem; color: var(--accent-purple); margin-bottom: 15px; font-weight: 800; }}
        .takeaways-card ul {{ list-style: none; padding: 0; }}
        .takeaways-card li {{ font-size: 1.05rem; color: #334155; margin-bottom: 12px; display: flex; align-items: center; }}
        .btn-back {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 28px;
            border-radius: 50px;
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: #fff;
            text-decoration: none;
            font-weight: 700;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2);
            transition: all 0.2s;
        }}
        .btn-back:hover {{ transform: translateY(-2px); opacity: 0.95; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="../index.html" class="logo"><i class="fa-solid fa-lightbulb"></i> الفكر الذكي</a>
        <a href="../index.html" style="color:var(--accent-purple); text-decoration:none; font-weight:700;"><i class="fa-solid fa-arrow-right"></i> الصفحة الرئيسية</a>
    </nav>
    
    <div class="container">
        <span class="category-badge"><i class="fa-solid fa-folder-open"></i> {category}</span>
        <h1>{title}</h1>
        <div class="meta">
            <span><i class="fa-regular fa-calendar"></i> تاريخ النشر: {today}</span>
            <span><i class="fa-regular fa-user"></i> {author}</span>
            <span><i class="fa-regular fa-clock"></i> وقت القراءة: 4 دقائق</span>
        </div>

        <div class="summary-box">
            {summary}
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

        <article class="article-body">
            {sections_html}
        </article>

        <div class="takeaways-card">
            <h4><i class="fa-solid fa-star"></i> النقاط الجوهرية للرفع من أدائك:</h4>
            <ul>
                {takeaways_html}
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

        <a href="../index.html" class="btn-back"><i class="fa-solid fa-arrow-right"></i> العودة للصفحة الرئيسية</a>
    </div>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"تم إنشاء المقال التفصيلي: {filename}")

if __name__ == "__main__":
    generate_article()
