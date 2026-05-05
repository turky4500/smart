<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>بلدي | المساعد الذكي للاشتراطات</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Tajawal', sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 0; }
        .app-container { width: 100%; max-width: 480px; height: 100vh; background: white; display: flex; flex-direction: column; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #0b3b5e, #134b6e); color: white; padding: 12px 18px; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
        .logo-text { font-weight: 800; font-size: 1.3rem; display: flex; align-items: center; gap: 5px; }
        .region-badge { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: bold; }
        .main-content { flex: 1; overflow-y: auto; padding: 12px 16px; background: #f9fafc; display: flex; flex-direction: column; gap: 12px; }
        .message { display: flex; gap: 8px; max-width: 90%; animation: fadeIn 0.25s ease; }
        .message.bot { align-self: flex-start; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .avatar { width: 32px; height: 32px; border-radius: 50%; background: #e9edf4; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .bot .avatar { background: #d9e8f5; color: #0b3b5e; }
        .user .avatar { background: #cde3d9; color: #1e4a3a; }
        .bubble { padding: 10px 14px; border-radius: 18px; font-size: 0.9rem; line-height: 1.6; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.05); word-break: break-word; }
        .user .bubble { background: #0b3b5e; color: white; }
        .input-area { display: flex; padding: 8px 12px; border-top: 1px solid #e2e8f0; background: white; gap: 8px; flex-shrink: 0; }
        .input-area input { flex: 1; border: 1px solid #dce2eb; border-radius: 24px; padding: 10px 16px; font-family: 'Tajawal', sans-serif; font-size: 0.85rem; outline: none; }
        .input-area button { background: #0b3b5e; color: white; border: none; width: 38px; height: 38px; border-radius: 50%; cursor: pointer; }
        .bottom-nav { display: flex; background: white; border-top: 1px solid #e2e8f0; padding: 6px 0; flex-shrink: 0; }
        .nav-item { flex: 1; text-align: center; color: #6b7c8e; font-size: 0.68rem; }
        .nav-item.active { color: #0b3b5e; font-weight: 600; }
        .error-chip { background: #ffe9e9; color: #a71d2a; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; display: inline-block; }
        .success-chip { background: #e8f5ed; color: #1a6e3e; padding: 2px 8px; border-radius: 12px; }
        .section-title { font-weight: 700; color: #0b3b5e; margin: 8px 0 4px; display: flex; align-items: center; gap: 6px; }
        .bubble ul { margin: 4px 0; padding-right: 18px; }
        .bubble li { margin: 3px 0; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        @media (min-width: 500px) { .app-container { border-radius: 28px; height: 90vh; max-height: 800px; } }
    </style>
</head>
<body>
<div class="app-container">
    <div class="header">
        <div class="logo-text"><i class="fas fa-city"></i> بلدي</div>
        <div class="region-badge">المساعد الذكي للتراخيص</div>
    </div>

    <div class="main-content" id="chatMessages"></div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="مثال: أريد فتح مطعم، أو محل أحذية..." onkeypress="handleKeyPress(event)" autofocus>
        <button onclick="sendMessage()"><i class="fas fa-arrow-left"></i></button>
    </div>

    <div class="bottom-nav">
        <div class="nav-item"><i class="fas fa-home"></i><br>الرئيسية</div>
        <div class="nav-item"><i class="fas fa-th-large"></i><br>الخدمات</div>
        <div class="nav-item active"><i class="fas fa-robot"></i><br>بلدي الذكي</div>
    </div>
</div>

<script>
    // 1. قم بلصق قيمة التوكن والكوكيز الخاصة بك هنا (كما هي بدون تغيير)
    const myCookies = "_ga=GA1.1.51101884.1761305085; _ga_RRB0N1LCS9=GS2.1.s1773507826$o21$g0$t1773507826$j60$l0$h0; TS0158fdf2=010bfa19f9c623838fba09ba365c468b633dbabf7a30e203749aa04219c8204abefc9235ad8b6a71bf8c0d166b2dd3831d0b09db0c; .ASPXFORMSAUTH=Yk1VWktwOENEMHE0UFQybGw4UVpVZz09; cto_bundle=Ja6N-l9KR0FjUFZuVCUyRm44cFI3JTJCV1NRakRhekJveVd4UTkyVmVoS09CZkZhRFY0R2RjM2NmTDBrdyUyRkklMkJxODVMeDRyaGZ4eW40NlhYQ3NLQVM4UzBnYXRNZENqTXRsVVZuJTJGR0Fib0VWMVZqaWx3N29NalNBVVZEa1lEaVRTNXVMWTNlSVlBc0wyTk9yYUIlMkZreWgxeG10JTJGaThVdyUzRCUzRA; _ga_94NSCR4KK1=GS2.1.s1778002969$o36$g0$t1778002971$j58$l0$h0; _ga_69XYTDF1T2=GS2.1.s1778002965$o82$g1$t1778002975$j50$l0$h0";
    const xsrfToken = "LdzqsqTvABLtLZfdwmaCN-qLTywRdJpNomgvIM7ozczVToNXura44RTC5wUpB83C6MN2754B-yQCOwtB907CVB_wC2Y1%3A2xWik4b9IgbVt0q4RCgzptCE-tWfvoLA5zGXIMwOBzvzPk92L1Y8jG9T8LbUcdaXIeJstT33TUfcDYHxuRbIqJRBKlA1";

    // 2. 📖 "قاموس الأنشطة" - هذا هو المفتاح لذكاء التطبيق (يمكنك إضافة المزيد هنا)
    const activityDictionary = {
        "مطعم": 836,    // مثال: عند كتابة مستخدم "مطعم"، سيتم تحويلها تلقائيًا للرقم 836
        "مقهى": 836,
        "بقالة": 835,
        "تموينات": 835,
        "محل احذية": 0,   // هذا مجرد مثال، تحتاج لاحقًا لاستخراج رقم النشاط الصحيح
        "مستودع": 0,
        "مقاولات": 0
    };

    // باقي كود التطبيق
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        const icon = sender === 'bot' ? 'fa-robot' : 'fa-user';
        div.innerHTML = `<div class="avatar"><i class="fas ${icon}"></i></div><div class="bubble">${text}</div>`;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function fetchActivityDetails(activityId) {
        const url = `https://services.balady.gov.sa/commercial/inquiry/ActivitiesInquiry/GetDetails?type=detailed&activityId=${activityId}`;
        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-XSRF-Token": xsrfToken,
                    "Cookie": myCookies,
                    "Referer": "https://services.balady.gov.sa/commercial/inquiry/ActivitiesInquiry"
                }
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const html = await response.text();
            return html;
        } catch (err) {
            console.error("Fetch error:", err);
            return null;
        }
    }

    function extractRegulationsFromHtml(html) {
        if (!html) return null;
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const text = tempDiv.innerText || tempDiv.textContent;
        const lines = text.split(/\r?\n/).filter(l => l.trim().length > 2).filter(l => !l.includes("تفاصيل النشاط") && !l.includes("إغلاق") && !l.includes("طبع"));
        if (lines.length === 0) return null;
        
        let formatted = `<div class="section-title"><i class="fas fa-check-circle"></i> تفاصيل النشاط من منصة بلدي</div>`;
        formatted += `<ul>`;
        for (let line of lines.slice(0, 35)) {
            let clean = line.trim();
            if (clean.length > 0) {
                formatted += `<li>${escapeHtml(clean.substring(0, 200))}</li>`;
            }
        }
        formatted += `</ul>`;
        formatted += `<div class="success-chip" style="margin-top:8px;"><i class="fas fa-database"></i> تم جلب البيانات مباشرة عبر API بلدي الرسمي</div>`;
        return formatted;
    }
    
    function escapeHtml(str) {
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }

    // 🧠 هذه هي الوظيفة الذكية التي تترجم كلام المستخدم إلى رقم النشاط
    function findActivityId(userMessage) {
        const lowerMsg = userMessage.toLowerCase();
        for (const [keyword, id] of Object.entries(activityDictionary)) {
            if (lowerMsg.includes(keyword)) {
                return id;
            }
        }
        return null; // لم نعثر على كلمة مفتاحية
    }

    async function sendMessage() {
        const input = userInput.value.trim();
        if (!input) return;
        addMessage(input, 'user');
        userInput.value = '';
        
        // 1. ترجمة كلام المستخدم إلى رقم النشاط
        const activityId = findActivityId(input);
        
        // 2. إذا لم يتم العثور على رقم مطابق
        if (activityId === null) {
            addMessage("عذرًا، لم أتعرف على النشاط الذي تبحث عنه. يمكنك تجربة كتابة 'مطعم'، 'مقهى'، 'بقالة'، أو 'تموينات'. سأقوم قريبًا بإضافة المزيد من الأنشطة مثل 'محل أحذية' و 'مستودع'.", 'bot');
            return;
        }

        // 3. إذا كان الرقم 0، فهذا يعني أن النشاط معروف لكن لم تتم إضافة رقمه بعد
        if (activityId === 0) {
            addMessage("شكرًا لك! لقد تعرفت على النشاط الذي تبحث عنه، ولكنه لم يتم ربطه برقم نشاط رسمي بعد في قاعدة البيانات. يمكنك مساعدتنا بإخباري برقم النشاط من موقع بلدي (apps.balady.gov.sa) وسأقوم بتحديثه.", 'bot');
            return;
        }
        
        // 4. إذا تم العثور على رقم صحيح، نقوم بجلب الاشتراطات
        addMessage(`🔄 جاري البحث عن نشاط "${input}" وجلب اشتراطاته من منصة بلدي ...`, 'bot');
        const htmlData = await fetchActivityDetails(activityId);
        
        if (htmlData && htmlData.length > 100 && !htmlData.includes("Login") && !htmlData.includes("خطأ")) {
            const formatted = extractRegulationsFromHtml(htmlData);
            if (formatted) {
                addMessage(formatted, 'bot');
            } else {
                addMessage("<span class='error-chip'>تم استلام بيانات ولكن لم نتمكن من تحليلها. قد يكون النشاط غير موجود أو البيانات مختلفة.</span>", 'bot');
            }
        } else {
            addMessage("<span class='error-chip'>فشل الاتصال أو انتهت صلاحية الجلسة. يرجى تحديث التوكن والكوكيز من المتصفح (كرر الخطوات السابقة) لأن التطبيق يحتاج إلى جلسة نشطة على منصة بلدي.</span>", 'bot');
        }
    }

    function handleKeyPress(e) {
        if (e.key === 'Enter') sendMessage();
    }

    window.addEventListener('DOMContentLoaded', () => {
        addMessage("السلام عليكم! أنا المساعد الذكي لاشتراطات الأنشطة التجارية.<br><br>📌 **كيف يمكنني مساعدتك؟**<br>• فقط اكتب ما تريد! مثال: <b>'أريد فتح مطعم'</b> أو <b>'مقهى'</b>.<br>• سأقوم بترجمة طلبك تلقائيًا وجلب الاشتراطات الرسمية من منصة بلدي لحظيًا.<br><br>✨ **ملاحظة:** التطبيق يعمل الآن مع (مطعم، مقهى، بقالة، تموينات). يمكننا إضافة المزيد بسهولة!", 'bot');
    });
</script>
</body>
</html>
