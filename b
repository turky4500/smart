<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>بلدي | المدقق الذكي الاستباقي</title>
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    body {
      background: #f4f6f9;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    .container {
      max-width: 900px;
      width: 100%;
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      padding: 30px 25px;
    }
    h1 {
      text-align: center;
      color: #0b3b5c;
      margin-bottom: 5px;
      font-size: 28px;
    }
    .subtitle {
      text-align: center;
      color: #2c7da0;
      margin-bottom: 30px;
      font-weight: 500;
    }
    .steps {
      display: flex;
      justify-content: space-between;
      margin-bottom: 35px;
      position: relative;
    }
    .step {
      text-align: center;
      flex: 1;
      position: relative;
      color: #aaa;
      font-weight: bold;
    }
    .step.active {
      color: #0b3b5c;
    }
    .step::before {
      content: attr(data-num);
      display: block;
      width: 35px;
      height: 35px;
      background: #ddd;
      border-radius: 50%;
      margin: 0 auto 8px;
      line-height: 35px;
      color: #fff;
      font-weight: bold;
      background: #aaa;
    }
    .step.active::before {
      background: #0b3b5c;
    }
    .step.done::before {
      background: #2a9d8f;
      content: "✓";
    }
    .panel {
      background: #f8fafc;
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 20px;
      border: 1px solid #e5e7eb;
    }
    label {
      display: block;
      margin-bottom: 6px;
      font-weight: 600;
      color: #1e293b;
    }
    select, input[type="text"], .fake-upload {
      width: 100%;
      padding: 12px 15px;
      border-radius: 10px;
      border: 1px solid #cbd5e1;
      font-size: 15px;
      background: #fff;
      margin-bottom: 15px;
    }
    .fake-upload {
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      color: #0b3b5c;
      font-weight: 500;
    }
    .row {
      display: flex;
      gap: 15px;
    }
    .row input {
      flex: 1;
    }
    #map {
      height: 280px;
      border-radius: 12px;
      border: 1px solid #cbd5e1;
      margin-bottom: 10px;
      z-index: 0;
    }
    .btn {
      background: #0b3b5c;
      color: #fff;
      border: none;
      padding: 12px 28px;
      border-radius: 30px;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
      margin-top: 10px;
    }
    .btn:hover {
      background: #145374;
    }
    .btn:disabled {
      background: #94a3b8;
      cursor: not-allowed;
    }
    .result-box {
      margin-top: 25px;
      padding: 20px;
      border-radius: 16px;
      font-weight: bold;
      text-align: center;
      font-size: 18px;
    }
    .result-success {
      background: #d1fae5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }
    .result-reject {
      background: #fee2e2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }
    .hint {
      font-size: 14px;
      color: #475569;
      margin-top: 8px;
    }
    .warning-text {
      color: #b91c1c;
      font-size: 14px;
    }
  </style>
</head>
<body>
<div class="container">
  <h1>🏛️ بلدي</h1>
  <div class="subtitle">المدقق الذكي الاستباقي · تدقيق فوري قبل الإرسال</div>

  <!-- مؤشر الخطوات -->
  <div class="steps">
    <div class="step active" data-num="1">النشاط والعقد</div>
    <div class="step" data-num="2">الموقع الجغرافي</div>
    <div class="step" data-num="3">نتيجة التدقيق</div>
  </div>

  <!-- الخطوة 1: النشاط والعقد -->
  <div class="panel" id="step1Panel">
    <label>📋 النشاط التجاري</label>
    <select id="activitySelect">
      <option value="">-- اختر النشاط --</option>
      <option value="بيع_تجزئة">بيع بالتجزئة (سوبر ماركت/ملابس)</option>
      <option value="مقهى">مقهى / كافيه</option>
      <option value="مخازن_عامة">مخازن عامة / مستودع</option>
      <option value="مطعم">مطعم</option>
    </select>

    <label style="margin-top:15px;">📄 رفع عقد الإيجار (محاكاة)</label>
    <div class="fake-upload" id="uploadTrigger">
      <span>📎 اضغط لرفع عقد الإيجار (PDF/صورة)</span>
      <span>⬆️</span>
    </div>
    <input type="file" id="realFileInput" accept=".pdf,.jpg,.png" style="display:none;">

    <div style="margin-top:15px;">
      <strong>البيانات المستخرجة تلقائياً:</strong>
      <div class="row" style="margin-top:10px;">
        <input type="text" id="tenantName" placeholder="اسم المستأجر" readonly>
        <input type="text" id="contractEndDate" placeholder="تاريخ نهاية العقد (هـ)" readonly>
      </div>
      <span id="contractWarning" class="warning-text"></span>
    </div>
  </div>

  <!-- الخطوة 2: الموقع -->
  <div class="panel" id="step2Panel" style="display:none;">
    <label>📍 حدد موقع المحل على الخريطة</label>
    <div id="map"></div>
    <div class="hint" id="selectedLocationText">لم يتم تحديد موقع بعد</div>
    <input type="hidden" id="selectedZone" value="">
  </div>

  <!-- زر التدقيق -->
  <div style="text-align: center; display: flex; justify-content: center; gap: 15px;">
    <button class="btn" id="nextStepBtn" onclick="goToStep2()">التالي: تحديد الموقع ←</button>
    <button class="btn" id="auditBtn" style="display:none;" onclick="runAudit()">🔍 تدقيق الطلب الآن</button>
  </div>

  <!-- نتيجة التدقيق -->
  <div id="resultContainer" style="display:none;"></div>
</div>

<!-- Leaflet JS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  // ---------- قاعدة المعرفة (اشتراطات الموقع) ----------
  const zoningRules = {
    "تجاري": ["بيع_تجزئة", "مقهى", "مطعم"],
    "مستودعات": ["مخازن_عامة"],
    "سكني": ["مقهى"] // مثال: فقط مقاهي صغيرة
  };

  // بيانات وهمية لمحاكاة عقد الإيجار
  const mockContractData = {
    tenant: "مؤسسة النخلة التجارية",
    endDate: "1448-06-14", // هجري
    valid: true
  };

  // ---------- حالة التطبيق ----------
  let currentStep = 1;
  let selectedActivity = "";
  let contractEndDate = "";
  let tenantName = "";
  let selectedZone = ""; // "تجاري" أو "مستودعات" أو "سكني"

  // تحديث واجهة الخطوات
  function updateStepsUI(activeStep) {
    document.querySelectorAll('.step').forEach((el, idx) => {
      el.classList.remove('active', 'done');
      if (idx + 1 === activeStep) el.classList.add('active');
      else if (idx + 1 < activeStep) el.classList.add('done');
    });
  }

  // الانتقال للخطوة الثانية
  function goToStep2() {
    selectedActivity = document.getElementById('activitySelect').value;
    tenantName = document.getElementById('tenantName').value.trim();
    contractEndDate = document.getElementById('contractEndDate').value.trim();

    // تحقق أساسي
    if (!selectedActivity) {
      alert("الرجاء اختيار النشاط التجاري أولاً");
      return;
    }
    if (!tenantName || !contractEndDate) {
      alert("الرجاء رفع عقد الإيجار لاستخراج البيانات تلقائياً");
      return;
    }
    // فحص تاريخ العقد (محاكاة بسيطة: نقارن بسنة 1448)
    if (contractEndDate < "1448-01-01") {
      document.getElementById('contractWarning').innerText = "⚠️ العقد منتهي الصلاحية! لا يمكن المتابعة.";
      return;
    } else {
      document.getElementById('contractWarning').innerText = "";
    }

    // إظهار لوحة الخريطة
    document.getElementById('step1Panel').style.display = 'none';
    document.getElementById('step2Panel').style.display = 'block';
    document.getElementById('nextStepBtn').style.display = 'none';
    document.getElementById('auditBtn').style.display = 'inline-block';
    currentStep = 2;
    updateStepsUI(2);
    // تأكد من تحميل الخريطة
    setTimeout(() => map.invalidateSize(), 100);
  }

  // ---------- الخريطة ----------
  const map = L.map('map').setView([24.7136, 46.6753], 13); // الرياض

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // إضافة منطقتين واضحتين (دوائر ملونة)
  const commercialZone = L.circle([24.7200, 46.6800], {
    color: '#2a9d8f',
    fillColor: '#2a9d8f',
    fillOpacity: 0.2,
    radius: 700
  }).addTo(map).bindPopup('🏢 منطقة تجارية (مسموح: بيع تجزئة، مقاهي، مطاعم)');

  const warehouseZone = L.circle([24.7050, 46.6600], {
    color: '#e76f51',
    fillColor: '#e76f51',
    fillOpacity: 0.2,
    radius: 700
  }).addTo(map).bindPopup('🏭 منطقة مستودعات (مسموح: مخازن عامة فقط)');

  // حدث النقر على الخريطة لتحديد الموقع
  let selectedMarker;
  map.on('click', function(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // إزالة العلامة القديمة
    if (selectedMarker) map.removeLayer(selectedMarker);

    // إضافة علامة جديدة
    selectedMarker = L.marker([lat, lng]).addTo(map)
      .bindPopup('📌 موقع المحل المحدد').openPopup();

    // تحديد المنطقة بناءً على المسافة من مراكز المناطق
    const distToCommercial = map.distance([lat, lng], commercialZone.getLatLng());
    const distToWarehouse = map.distance([lat, lng], warehouseZone.getLatLng());

    if (distToCommercial < 800) {
      selectedZone = "تجاري";
      document.getElementById('selectedLocationText').innerHTML = '✅ تم اختيار موقع داخل <strong>المنطقة التجارية</strong>';
    } else if (distToWarehouse < 800) {
      selectedZone = "مستودعات";
      document.getElementById('selectedLocationText').innerHTML = '⚠️ تم اختيار موقع داخل <strong>منطقة المستودعات</strong>';
    } else {
      selectedZone = "سكني"; // افتراضي
      document.getElementById('selectedLocationText').innerHTML = '📍 موقع خارج المناطق المحددة (يعامل كـ سكني مؤقتاً)';
    }

    document.getElementById('selectedZone').value = selectedZone;
  });

  // ---------- رفع عقد الإيجار (محاكاة) ----------
  document.getElementById('uploadTrigger').addEventListener('click', function() {
    // محاكاة قراءة الملف واستخراج البيانات (في الواقع سنستخدم بيانات وهمية)
    document.getElementById('tenantName').value = mockContractData.tenant;
    document.getElementById('contractEndDate').value = mockContractData.endDate;
    document.getElementById('contractWarning').innerText = "";
    alert("✅ تم تحليل العقد بنجاح (محاكاة). البيانات المستخرجة: " + mockContractData.tenant + " - ينتهي " + mockContractData.endDate);
  });

  // لو أردت استخدام ملف حقيقي (يُترك شكلياً)
  document.getElementById('realFileInput').addEventListener('change', function(e) {
    // في النسخة الحقيقية هنا تأتي مكتبة OCR أو قراءة PDF
    // حالياً نستخدم نفس المحاكاة
    document.getElementById('tenantName').value = mockContractData.tenant;
    document.getElementById('contractEndDate').value = mockContractData.endDate;
    alert("📄 تم فحص الملف (محاكاة التعرف البصري).");
  });

  // ---------- التدقيق والفحص ----------
  function runAudit() {
    selectedActivity = document.getElementById('activitySelect').value;
    selectedZone = document.getElementById('selectedZone').value || selectedZone;

    if (!selectedZone) {
      alert("الرجاء النقر على الخريطة لتحديد موقع المحل");
      return;
    }

    const allowedActivities = zoningRules[selectedZone] || [];
    const isAllowed = allowedActivities.includes(selectedActivity);

    const resultDiv = document.getElementById('resultContainer');
    resultDiv.style.display = 'block';

    // اسم النشاط بالعربية للعرض
    const activityNames = {
      "بيع_تجزئة": "بيع بالتجزئة",
      "مقهى": "مقهى",
      "مخازن_عامة": "مخازن عامة",
      "مطعم": "مطعم"
    };
    const zoneNames = {
      "تجاري": "تجارية",
      "مستودعات": "مستودعات",
      "سكني": "سكنية"
    };

    if (isAllowed) {
      resultDiv.innerHTML = `
        <div class="result-box result-success">
          ✅ متوافق مع الاشتراطات<br>
          <small>النشاط "${activityNames[selectedActivity]}" مسموح به في المنطقة ${zoneNames[selectedZone]}.</small><br>
          <small style="color:#065f46;">يمكنك متابعة تقديم الطلب.</small>
        </div>`;
    } else {
      // اقتراح النشاط المناسب إذا كانت القواعد تحدد شيئاً
      let suggestion = "";
      if (selectedZone === "مستودعات") {
        suggestion = "النشاط المسموح في هذه المنطقة هو: مخازن عامة فقط.";
      } else if (selectedZone === "سكني") {
        suggestion = "الأنشطة المسموحة في المنطقة السكنية: مقاهي فقط (حسب الاشتراطات).";
      } else {
        suggestion = "يرجى مراجعة اشتراطات المخطط.";
      }

      resultDiv.innerHTML = `
        <div class="result-box result-reject">
          🚫 غير مسموح بهذا النشاط في الموقع المحدد<br>
          <small>النشاط "${activityNames[selectedActivity]}" لا يتوافق مع المنطقة ${zoneNames[selectedZone]}.</small><br>
          <small style="font-weight:bold;">${suggestion}</small>
        </div>`;
    }

    // الانتقال للخطوة 3 شكلياً
    updateStepsUI(3);
    document.getElementById('auditBtn').disabled = true;
  }

  // إعادة تعيين بسيطة عند تغيير النشاط (اختياري)
  document.getElementById('activitySelect').addEventListener('change', function() {
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('auditBtn').disabled = false;
  });

  // للسماح برفع ملف حقيقي عند النقر على الزر المزيف (اختياري)
  document.getElementById('uploadTrigger').addEventListener('dblclick', function() {
    document.getElementById('realFileInput').click();
  });
</script>
</body>
</html>
