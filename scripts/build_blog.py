# -*- coding: utf-8 -*-
"""Build only the blog pages. Does not touch the other tools in the repo."""
import os
import re
import datetime
import html
from articles_data import ARTICLES
from article_expansions import EXTRA
from article_walkthroughs import WALK

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://turky4500.github.io/smart"
PUB = "ca-pub-7778135355055222"
SLOT = "5093830951"
AUTHOR = "فريق التحرير"

MONTHS = {
    1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
    7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر",
}

NAV = [
    ("index.html", "الرئيسية"),
    ("index.html#articles", "المقالات"),
    ("about.html", "من نحن"),
    ("contact.html", "تواصل"),
    ("privacy.html", "الخصوصية"),
]


def arabic_date(iso):
    y, m, d = [int(x) for x in iso.split("-")]
    return f"{d} {MONTHS[m]} {y}"


def read_minutes(article):
    text = article["title"] + article["description"]
    for title, paras in article["sections"]:
        text += title + "".join(paras)
    words = max(1, len(text.split()))
    return max(6, round(words / 110))


def by_file():
    return {a["file"]: a for a in ARTICLES}


def expanded(article):
    extra = list(EXTRA.get(article["file"], [])) + list(WALK.get(article["file"], []))
    if not extra:
        return article
    merged = dict(article)
    merged["sections"] = list(article["sections"]) + extra
    return merged


def ad_box():
    return f"""
    <div class="ad-box">
      <div class="ad-label">إعلان</div>
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="{PUB}"
           data-ad-slot="{SLOT}"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>"""


def head(title, description, canonical, prefix, extra="", og_type="website"):
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="author" content="{AUTHOR}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="ar" href="{canonical}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:site_name" content="مدونة الفكر الذكي">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta name="theme-color" content="#5b21b6">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="{prefix}blog.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>
  {extra}
</head>"""


def nav_html(prefix, active):
    items = []
    for href, label in NAV:
        cls = ' class="active"' if label == active else ""
        items.append(f'<li><a href="{prefix}{href}"{cls}>{label}</a></li>')
    return f"""
  <a class="skip-link" href="#main">تجاوز إلى المحتوى</a>
  <header class="site-header">
    <div class="nav-wrap">
      <a class="logo" href="{prefix}index.html">
        <span class="logo-mark"><i class="fa-solid fa-lightbulb"></i></span>
        الفكر الذكي
      </a>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links">القائمة</button>
      <ul class="nav-links" id="nav-links">
        {''.join(items)}
      </ul>
    </div>
  </header>"""


def footer_html(prefix):
    return f"""
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <h3>مدونة الفكر الذكي</h3>
        <p>مدونة عربية مستقلة تكتب شروحًا عملية عن التقنية اليومية، الأمان الرقمي، وتنظيم العمل والدراسة. نكتب للقارئ غير المتخصص، ونراجع كل مقال قبل نشره.</p>
        <p>التواصل: <a href="mailto:tur100@gmail.com">tur100@gmail.com</a></p>
      </div>
      <div>
        <h3>تصفح</h3>
        <ul>
          <li><a href="{prefix}index.html">الرئيسية</a></li>
          <li><a href="{prefix}about.html">من نحن</a></li>
          <li><a href="{prefix}contact.html">تواصل معنا</a></li>
        </ul>
      </div>
      <div>
        <h3>الصفحات القانونية</h3>
        <ul>
          <li><a href="{prefix}privacy.html">سياسة الخصوصية</a></li>
          <li><a href="{prefix}disclaimer.html">إخلاء المسؤولية</a></li>
          <li><a href="{prefix}sitemap.xml">خريطة الموقع</a></li>
        </ul>
      </div>
    </div>
    <div class="copy">© {datetime.date.today().year} مدونة الفكر الذكي — محتوى أصلي مستقل</div>
  </footer>
  <div class="cookie" id="cookie-banner">
    <p>نستخدم ملفات تعريف الارتباط لعرض الإعلانات عبر Google وقياس استخدام الصفحات. راجع <a href="{prefix}privacy.html">سياسة الخصوصية</a>.</p>
    <button type="button" id="cookie-ok">حسنًا</button>
  </div>
  <script src="{prefix}blog.js"></script>
</body>
</html>"""


def schema_website():
    return f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "مدونة الفكر الذكي",
    "inLanguage": "ar",
    "url": "{SITE}/",
    "description": "شروح عربية عملية عن التقنية اليومية والأمان الرقمي والإنتاجية.",
    "publisher": {{
      "@type": "Organization",
      "name": "مدونة الفكر الذكي",
      "url": "{SITE}/"
    }}
  }}
  </script>"""


def schema_article(article, url):
    return f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {html.escape(article['title']).join(['"', '"']) if False else '"' + article['title'].replace('"', '\\"') + '"'},
    "description": "{article['description'].replace('"', '\\"')}",
    "inLanguage": "ar",
    "datePublished": "{article['date']}",
    "dateModified": "{article['date']}",
    "author": {{"@type": "Organization", "name": "{AUTHOR}"}},
    "publisher": {{"@type": "Organization", "name": "مدونة الفكر الذكي", "url": "{SITE}/"}},
    "mainEntityOfPage": "{url}",
    "articleSection": "{article['category']}"
  }}
  </script>"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) if os.path.dirname(full) else ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def build_index():
    cats = ["الكل"] + sorted({a["category"] for a in ARTICLES})
    filters = []
    for i, c in enumerate(cats):
        cls = "filter-btn active" if i == 0 else "filter-btn"
        filters.append(f'<button class="{cls}" type="button" data-filter="{html.escape(c)}">{html.escape(c)}</button>')

    cards = []
    for a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True):
        cards.append(f"""
        <article class="card" data-category="{html.escape(a['category'])}">
          <div class="card-top"><i class="fa-solid {a['icon']}"></i></div>
          <div class="card-body">
            <span class="tag">{html.escape(a['category'])}</span>
            <h3><a href="posts/{a['file']}">{html.escape(a['title'])}</a></h3>
            <p class="excerpt">{html.escape(a['excerpt'])}</p>
            <div class="card-meta">
              <span>{arabic_date(a['date'])}</span>
              <a href="posts/{a['file']}">اقرأ المقال</a>
            </div>
          </div>
        </article>""")

    page = f"""{head("مدونة الفكر الذكي — شروح عملية للتقنية اليومية", "مدونة عربية مستقلة تقدم شروحًا واضحة عن الأمان الرقمي، تنظيم الملفات، وحماية الحسابات للفرد والأسرة.", f"{SITE}/", "", schema_website())}
<body>
{nav_html("", "الرئيسية")}
  <main id="main" class="wrap">
    <section class="hero">
      <div class="eyebrow"><i class="fa-solid fa-feather"></i> مدونة مستقلة — نكتب للقارئ لا للإعلان</div>
      <h1>شروح هادئة تساعدك تستخدم التقنية بثقة</h1>
      <p>هنا مقالات عملية عن حماية الحسابات، نسخ الصور، تنظيم العمل والدراسة، وضبط إعدادات الجوال والبيت. نكتب بلغة واضحة، ونبتعد عن الحيل والوعود السريعة.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#articles">تصفح المقالات</a>
        <a class="btn btn-ghost" href="about.html">تعرّف على المدونة</a>
      </div>
    </section>
  </main>
  {ad_box()}
  <section class="wrap" id="articles">
    <div class="section-head">
      <h2>المقالات</h2>
      <span style="color:var(--muted);font-weight:700">{len(ARTICLES)} مقالًا أصليًا</span>
    </div>
    <div class="filters">{''.join(filters)}</div>
    <div class="grid" id="posts-list">
      <!-- POSTS_START -->
      {''.join(cards)}
      <!-- POSTS_END -->
    </div>
  </section>
  <section class="wrap" style="margin:48px auto 10px;max-width:800px">
    <h2>كيف نكتب؟</h2>
    <p class="lead">كل مقال يعالج موقفًا يوميًا واحدًا، بخطوات يمكن تطبيقها في الجلسة نفسها. لا نعيد نشر قوالب جاهزة، ولا نكتب عن «مضاعفة الأرباح» أو حيل الظهور السريع. إن احتجت توضيحًا أو تصحيحًا، راسلنا من صفحة التواصل.</p>
  </section>
{footer_html("")}"""
    write("index.html", page)


def related_title(filename):
    name = os.path.basename(filename)
    path = os.path.join(ROOT, "posts", name)
    if not os.path.exists(path):
        lookup = by_file()
        if name in lookup:
            return lookup[name]["title"]
        return None
    with open(path, encoding="utf-8") as f:
        html_text = f.read()
    m = re.search(r"<h1>(.*?)</h1>", html_text, re.S)
    if not m:
        return None
    return re.sub(r"\s+", " ", m.group(1)).strip()


def write_post(a):
    import json
    url = f"{SITE}/posts/{a['file']}"
    sections = []
    for i, (title, paras) in enumerate(a["sections"]):
        block = f"<h2>{html.escape(title)}</h2>" + "".join(f"<p>{html.escape(p)}</p>" for p in paras)
        sections.append(block)
        if i == 1:
            sections.append(ad_box())

    takes = "".join(f"<li>{html.escape(t)}</li>" for t in a.get("takeaways", []))
    faqs = []
    faq_schema = []
    for q, ans in a.get("faqs", []):
        faqs.append(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(ans)}</p></details>")
        faq_schema.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": ans},
        })

    related = []
    for rf in a.get("related", []):
        title = related_title(rf)
        if title:
            related.append(f'<a href="{os.path.basename(rf)}">{html.escape(title)}</a>')

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema,
    }, ensure_ascii=False)

    extra = schema_article(a, url) + f'\n  <script type="application/ld+json">{faq_json}</script>'
    mins = read_minutes(a)
    page = f"""{head(a['title'] + " | مدونة الفكر الذكي", a['description'], url, "../", extra, "article")}
<body>
{nav_html("../", "المقالات")}
  <main id="main" class="wrap">
    <article class="page">
      <nav class="breadcrumb"><a href="../index.html">الرئيسية</a> / <a href="../index.html#articles">{html.escape(a['category'])}</a></nav>
      <span class="tag">{html.escape(a['category'])}</span>
      <h1>{html.escape(a['title'])}</h1>
      <div class="meta">
        <span><i class="fa-regular fa-calendar"></i> {arabic_date(a['date'])}</span>
        <span><i class="fa-regular fa-user"></i> {AUTHOR}</span>
        <span><i class="fa-regular fa-clock"></i> {mins} دقائق قراءة</span>
      </div>
      <p class="summary">{html.escape(a['excerpt'])}</p>
      <div class="article-body">
        {''.join(sections)}
        <div class="callout">
          <h3>خلاصة سريعة</h3>
          <ul>{takes}</ul>
        </div>
        <h2>أسئلة شائعة</h2>
        <div class="faq">{''.join(faqs)}</div>
        <h2>اقرأ أيضًا</h2>
        <div class="related">{''.join(related)}</div>
      </div>
      {ad_box()}
      <p style="margin-top:18px"><a class="btn btn-primary" href="../index.html">العودة لكل المقالات</a></p>
    </article>
  </main>
{footer_html("../")}"""
    write(f"posts/{a['file']}", page)


def build_posts():
    for raw in ARTICLES:
        write_post(expanded(raw))


def build_static():
    about = f"""{head("من نحن | مدونة الفكر الذكي", "مدونة عربية مستقلة تكتب شروحًا عملية عن التقنية اليومية والأمان الرقمي من الرياض.", f"{SITE}/about.html", "")}
<body>
{nav_html("", "من نحن")}
  <main id="main" class="wrap">
    <article class="page legal">
      <h1>من نحن</h1>
      <p><strong>مدونة الفكر الذكي</strong> منصة تحريرية مستقلة تُكتب بالعربية. هدفها مساعدة القارئ غير المتخصص على استخدام التقنية بثقة: حماية الحسابات، حفظ الصور، تنظيم الملفات، وفهم الإعدادات اليومية للجوال والبيت.</p>
      <h2>ماذا ننشر؟</h2>
      <p>مقالات عملية قصيرة بما يكفي لتُقرأ في جلسة، وطويلة بما يكفي لتنفيذ الخطوات دون الرجوع لعشر مصادر. نتجنب محتوى الحيل السريعة، ووعود الربح، وإعادة صياغة المقالات نفسها بعناوين مختلفة.</p>
      <h2>من يكتب؟</h2>
      <p>المحتوى يصدر باسم <strong>فريق التحرير</strong>. نراجع المقال قبل نشره من جهة اللغة ووضوح الخطوات، ونحدّثه إذا تغيّر أسلوب شائع في التطبيقات. لسنا جهة حكومية، ولسنا مرتبطين بمنصة بلدي أو أمانة أو أي تطبيق رسمي يظهر في ملفات أخرى داخل الاستضافة.</p>
      <h2>أين نكتب؟</h2>
      <p>التحرير من الرياض، المملكة العربية السعودية. اللغة عربية فصحى قريبة من الاستخدام اليومي في الخليج.</p>
      <h2>تواصل</h2>
      <p>للتصويب أو الاقتراح راسل <a href="mailto:tur100@gmail.com">tur100@gmail.com</a> أو استخدم <a href="contact.html">صفحة التواصل</a>. نرحب بالتنبيه على أي خطوة أصبحت قديمة بعد تحديث تطبيق.</p>
    </article>
  </main>
{footer_html("")}"""
    write("about.html", about)

    privacy = f"""{head("سياسة الخصوصية | مدونة الفكر الذكي", "كيف نتعامل مع البيانات وملفات تعريف الارتباط وإعلانات Google في مدونة الفكر الذكي.", f"{SITE}/privacy.html", "")}
<body>
{nav_html("", "الخصوصية")}
  <main id="main" class="wrap">
    <article class="page legal">
      <h1>سياسة الخصوصية</h1>
      <p>آخر تحديث: 19 أغسطس 2026. تنطبق هذه السياسة على صفحات مدونة الفكر الذكي على العنوان {SITE}/.</p>
      <h2>من المسؤول عن هذه الصفحات</h2>
      <p>مدونة الفكر الذكي مدونة مستقلة. للاستفسار عن الخصوصية راسلنا على <a href="mailto:tur100@gmail.com">tur100@gmail.com</a> أو عبر <a href="contact.html">صفحة التواصل</a>.</p>
      <h2>ما البيانات التي قد تُجمع</h2>
      <p>المدونة صفحات ثابتة. نحن لا نطلب إنشاء حساب ولا نبيع منتجات عبر هذه الصفحات. إذا أرسلت رسالة من نموذج التواصل فستصل عبر برنامج البريد على جهازك، ونحتفظ فقط بما ترسله إلينا للرد عليك.</p>
      <p>ملفات السجلات التقنية المعتادة (مثل عنوان IP تقريبي ونوع المتصفح) قد تُسجَّل لدى جهة الاستضافة أو أدوات القياس أثناء فتح الصفحة.</p>
      <h2>الإعلانات وملفات تعريف الارتباط</h2>
      <p>نعرض إعلانات عبر Google AdSense. وفق متطلبات Google:</p>
      <ul>
        <li>يستخدم موردون خارجيون، ومنهم Google، ملفات تعريف الارتباط لعرض إعلانات بناءً على زيارات المستخدم السابقة لهذا الموقع أو لمواقع أخرى.</li>
        <li>يتيح استخدام Google لملفات تعريف الارتباط الإعلانية له ولشركائه عرض إعلانات للمستخدمين بناءً على زيارتهم لمواقعنا و/أو مواقع أخرى على الإنترنت.</li>
        <li>يمكن للمستخدمين إلغاء الإعلانات المخصصة عبر <a href="https://www.google.com/settings/ads" rel="noopener" target="_blank">إعدادات الإعلانات في Google</a>، أو إلغاء استخدام بعض الموردين الخارجيين لملفات تعريف الارتباط عبر <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">www.aboutads.info</a>.</li>
      </ul>
      <p>قد يستخدم موردون أو شبكات إعلانية أخرى ملفات تعريف ارتباط لعرض إعلانات على الموقع إذا لم يتم إيقاف عرض الإعلانات من أطراف ثالثة. يمكنك مراجعة سياسات أولئك الموردين من مواقعهم وإلغاء الاشتراك إن وفروا ذلك.</p>
      <h2>القياس</h2>
      <p>قد نستخدم أدوات قياس بسيطة لفهم أي المقالات يُقرأ أكثر. هذه الأدوات قد تضع ملف تعريف ارتباط أو تعتمد على عنوان تقريبي. لا نستخدمها لبيع بياناتك.</p>
      <h2>الروابط الخارجية</h2>
      <p>قد يشير المقال إلى مواقع أخرى. سياسات تلك المواقع مستقلة عنا.</p>
      <h2>الأطفال</h2>
      <p>المحتوى موجّه للكبار ولأولياء الأمور. لا نجمع بيانات عن الأطفال عن قصد.</p>
      <h2>التعديلات</h2>
      <p>قد نحدّث هذه الصفحة عند تغيّر طريقة عمل الإعلانات أو الاستضافة. تاريخ التحديث يظهر في أعلى الصفحة.</p>
    </article>
  </main>
{footer_html("")}"""
    write("privacy.html", privacy)

    contact = f"""{head("تواصل معنا | مدونة الفكر الذكي", "راسل فريق تحرير مدونة الفكر الذكي للتصويب أو اقتراح موضوع.", f"{SITE}/contact.html", "")}
<body>
{nav_html("", "تواصل")}
  <main id="main" class="wrap">
    <article class="page legal">
      <h1>تواصل معنا</h1>
      <p>للتصويب على خطوة في مقال، أو اقتراح موضوع يناسب القارئ غير المتخصص، راسلنا على <a href="mailto:tur100@gmail.com">tur100@gmail.com</a> أو استخدم النموذج أدناه. نقرأ الرسائل المتعلقة بالمحتوى، ولا نقدم دعمًا فنيًا لحسابات البنوك أو الجهات الرسمية.</p>
      <form class="form" id="contact-form">
        <div>
          <label for="name">الاسم</label>
          <input id="name" name="name" required maxlength="80" autocomplete="name">
        </div>
        <div>
          <label for="email">بريدك الإلكتروني</label>
          <input id="email" name="email" type="email" required maxlength="120" autocomplete="email">
        </div>
        <div>
          <label for="message">الرسالة</label>
          <textarea id="message" name="message" rows="7" required maxlength="4000"></textarea>
        </div>
        <button class="btn btn-primary" type="submit">إرسال</button>
        <p id="form-status"></p>
      </form>
      <h2>قبل المراسلة</h2>
      <p>إذا كان سؤالك عن احتيال مالي أو حساب مسروق، تواصل مع البنك أو الجهة الرسمية من داخل تطبيقهم، لا عبر روابط وصلت في رسالة.</p>
    </article>
  </main>
{footer_html("")}"""
    write("contact.html", contact)

    disc = f"""{head("إخلاء المسؤولية | مدونة الفكر الذكي", "حدود الاستفادة من مقالات مدونة الفكر الذكي.", f"{SITE}/disclaimer.html", "")}
<body>
{nav_html("", "")}
  <main id="main" class="wrap">
    <article class="page legal">
      <h1>إخلاء المسؤولية</h1>
      <p>المقالات لأغراض التثقيف العام. أسماء التطبيقات والإعدادات تتغير مع التحديثات، وقد يختلف مكان الزر من جهاز لآخر. راجع دائمًا شاشة جهازك ولا تعتمد على المقال كاستشارة قانونية أو مالية أو أمنية شاملة.</p>
      <p>لا نتحمل مسؤولية قرارات تُتخذ بناءً على قراءة المقال وحده، خصوصًا في المعاملات المالية أو حماية حسابات العمل.</p>
      <p>الإعلانات التي تظهر عبر Google تُدار وفق سياسات Google، وقد تكون ذات صلة بموضوع الصفحة أو بزيارات سابقة. ظهور إعلان لا يعني تزكية المنتج.</p>
      <p>المدونة مستقلة وليست واجهة لأي جهة حكومية أو تطبيق رسمي.</p>
    </article>
  </main>
{footer_html("")}"""
    write("disclaimer.html", disc)


def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = [
        ("index.html", "1.0", today),
        ("about.html", "0.6", today),
        ("contact.html", "0.5", today),
        ("privacy.html", "0.5", today),
        ("disclaimer.html", "0.4", today),
    ]
    for a in ARTICLES:
        urls.append((f"posts/{a['file']}", "0.8", a["date"]))
    body = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, last in urls:
        loc = f"{SITE}/{path}" if path != "index.html" else f"{SITE}/"
        body.append(f"  <url><loc>{loc}</loc><lastmod>{last}</lastmod><priority>{pri}</priority></url>")
    body.append("</urlset>\n")
    write("sitemap.xml", "\n".join(body))


def build_favicon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#5b21b6"/>
  <path fill="#fff" d="M32 12c-8 0-14 6.2-14 14 0 5.4 3 10 7.4 12.4L24 46h16l-1.4-7.6C43 36 46 31.4 46 26c0-7.8-6-14-14-14zm-6 38h12v4H26z"/>
</svg>"""
    write("favicon.svg", svg)


if __name__ == "__main__":
    build_favicon()
    build_index()
    build_posts()
    build_static()
    build_sitemap()
    print("blog build complete", len(ARTICLES), "articles")
