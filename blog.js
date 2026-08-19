(function () {
  var btn = document.getElementById("menu-btn");
  var links = document.getElementById("nav-links");
  if (btn && links) {
    btn.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var filters = document.querySelectorAll(".filter-btn");
  var cards = document.querySelectorAll("[data-category]");
  filters.forEach(function (f) {
    f.addEventListener("click", function () {
      filters.forEach(function (x) { x.classList.remove("active"); });
      f.classList.add("active");
      var cat = f.getAttribute("data-filter");
      cards.forEach(function (card) {
        var show = cat === "الكل" || card.getAttribute("data-category") === cat;
        card.style.display = show ? "" : "none";
      });
    });
  });

  var cookie = document.getElementById("cookie-banner");
  if (cookie && !localStorage.getItem("smart-cookie-ok")) {
    cookie.style.display = "flex";
    var ok = document.getElementById("cookie-ok");
    if (ok) {
      ok.addEventListener("click", function () {
        localStorage.setItem("smart-cookie-ok", "1");
        cookie.style.display = "none";
      });
    }
  }

  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = document.getElementById("name").value.trim();
      var email = document.getElementById("email").value.trim();
      var msg = document.getElementById("message").value.trim();
      var status = document.getElementById("form-status");
      if (!name || !email || !msg) {
        status.textContent = "فضلاً أكمل كل الحقول قبل الإرسال.";
        return;
      }
      var body = encodeURIComponent("الاسم: " + name + "\nالبريد: " + email + "\n\n" + msg);
      var subject = encodeURIComponent("رسالة من مدونة الفكر الذكي");
      status.innerHTML = "تم تجهيز الرسالة على جهازك. إذا لم يفتح برنامج البريد، انسخ النص وأرسله يدويًا.";
      window.location.href = "mailto:tur100@gmail.com?subject=" + subject + "&body=" + body;
    });
  }
})();
