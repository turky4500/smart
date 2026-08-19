# -*- coding: utf-8 -*-
"""Generate one unique Arabic article via Gemini. Stdlib only."""
import json
import os
import re
import urllib.error
import urllib.request

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash",
]

BANNED = [
    "adsense", "أدسنس", "ادسنس", "أرباح الإعلان", "ربح من الإعلان",
    "high cpc", "كلمات مفتاحية ربحية", "سيو", "seo", "تسويق بالعمولة",
    "مضاعفة الأرباح", "مليونير", "get rich", "domain authority",
    "rpm", "ctr الإعلان",
]

CATEGORIES = ["أمان رقمي", "حياة رقمية", "مهارات تقنية", "إنتاجية", "تعليم تقني"]


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no json object in model output")
    return json.loads(text[start:end + 1])


def call_gemini(prompt, api_key):
    last_error = None
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 4096,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    for model in MODELS:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return extract_json(text), model
        except Exception as exc:
            last_error = f"{model}: {exc}"
            print("Gemini model failed:", last_error)
    raise RuntimeError(last_error or "all Gemini models failed")


def too_similar(title, existing):
    words = [w for w in re.split(r"\s+", title) if len(w) > 2]
    for other in existing:
        owords = [w for w in re.split(r"\s+", other) if len(w) > 2]
        if not words or not owords:
            continue
        overlap = len(set(words) & set(owords)) / max(len(set(words)), 1)
        if overlap >= 0.72:
            return True
        if title.strip() == other.strip():
            return True
    return False


def looks_bad(article):
    blob = json.dumps(article, ensure_ascii=False).lower()
    for word in BANNED:
        if word.lower() in blob:
            return f"banned term: {word}"
    title = (article.get("title") or "").strip()
    if len(title) < 12:
        return "title too short"
    if article.get("category") not in CATEGORIES:
        return "bad category"
    sections = article.get("sections") or []
    if len(sections) < 4:
        return "not enough sections"
    text_len = 0
    for sec in sections:
        heading = sec.get("heading") or ""
        paras = sec.get("paragraphs") or []
        if not heading or len(paras) < 1:
            return "empty section"
        text_len += len(heading) + sum(len(p) for p in paras)
    if text_len < 900:
        return "article too thin"
    if len(article.get("takeaways") or []) < 3:
        return "missing takeaways"
    if len(article.get("faqs") or []) < 2:
        return "missing faqs"
    return None


def build_prompt(topic, existing_titles):
    sample = " | ".join(list(existing_titles)[:25])
    cats = "، ".join(CATEGORIES)
    return f"""اكتب مقالًا عربيًا عمليًا أصليًا لمدونة «الفكر الذكي».
الموضوع المقترح: {topic}

الجمهور: قارئ غير متخصص في السعودية والخليج.
الأسلوب: فصحى قريبة من الكلام اليومي، هادئ، خطوات واضحة، بلا حشو وبلا وعود ربح.
ممنوع تمامًا: أدسنس، أرباح الإعلانات، السيو، الكلمات المفتاحية الربحية، الثراء السريع، تكرار مقال موجود.

عناوين موجودة لا تكررها ولا تقاربها:
{sample}

أرجع JSON فقط بهذا الشكل:
{{
  "title": "عنوان عربي واضح بدون خط عمودي",
  "category": "واحد فقط من: {cats}",
  "icon": "fa-solid icon name مثل fa-shield-halved",
  "excerpt": "جملتان قصيرتان",
  "description": "وصف ميتا حتى 160 حرفًا",
  "sections": [
    {{"heading": "عنوان قسم", "paragraphs": ["فقرة", "فقرة"]}}
  ],
  "takeaways": ["خلاصة", "خلاصة", "خلاصة", "خلاصة"],
  "faqs": [{{"q": "سؤال", "a": "جواب قصير"}}]
}}

المطلوب 5 أقسام على الأقل، فقرتان في كل قسم، 3 أسئلة شائعة. لا تضع ماركداون خارج JSON."""


def article_from_model(raw):
    sections = []
    for sec in raw.get("sections") or []:
        heading = (sec.get("heading") or "").strip()
        paras = [p.strip() for p in (sec.get("paragraphs") or []) if str(p).strip()]
        if heading and paras:
            sections.append((heading, paras))
    faqs = []
    for item in raw.get("faqs") or []:
        q = (item.get("q") or item.get("question") or "").strip()
        a = (item.get("a") or item.get("answer") or "").strip()
        if q and a:
            faqs.append((q, a))
    icon = (raw.get("icon") or "fa-lightbulb").replace("fa-solid", "").strip()
    if not icon.startswith("fa-"):
        icon = "fa-lightbulb"
    return {
        "title": (raw.get("title") or "").strip(),
        "category": (raw.get("category") or "مهارات تقنية").strip(),
        "icon": icon,
        "excerpt": (raw.get("excerpt") or "").strip(),
        "description": (raw.get("description") or "").strip(),
        "sections": sections,
        "takeaways": [t.strip() for t in (raw.get("takeaways") or []) if str(t).strip()],
        "faqs": faqs,
        "related": [],
    }


def generate_article(topic, existing_titles, api_key=None):
    api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")
    raw, model = call_gemini(build_prompt(topic, existing_titles), api_key)
    article = article_from_model(raw)
    reason = looks_bad(article)
    if reason:
        raise RuntimeError(f"quality check failed ({reason})")
    if too_similar(article["title"], existing_titles):
        raise RuntimeError("title too similar to an existing article")
    article["_model"] = model
    article["_topic"] = topic
    return article
