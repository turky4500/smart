// app.js

// مصفوفة لتخزين أسماء الشركات المقروءة من ملف CSV
let companies = [];

// تهيئة عناصر الصفحة بعد التحميل الكامل
document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    loadCompaniesCSV();
});

// 1. جلب وقراءة ملف CSV
async function loadCompaniesCSV() {
    try {
        // جلب الملف من المجلد (أو المستودع على GitHub)
        const response = await fetch('companies.csv');
        if (!response.ok) {
            throw new Error("فشل في تحميل ملف companies.csv.");
        }
        
        const csvText = await response.text();
        parseCSV(csvText);
    } catch (error) {
        console.error("Error loading CSV:", error);
        const noResults = document.getElementById("no-results");
        noResults.textContent = "خطأ: تعذر تحميل ملف الشركات المعتمدة (companies.csv). يرجى التأكد من رفع ملف الـ CSV في المستودع.";
        noResults.style.display = "block";
    }
}

// 2. تحليل نصوص الـ CSV المكونة من عمود واحد (أسماء الشركات)
function parseCSV(text) {
    // تقسيم النص إلى أسطر وتصفية الأسطر الفارغة
    const lines = text.split(/\r?\n/).filter(line => line.trim() !== "");
    
    if (lines.length <= 1) {
        document.getElementById("no-results").textContent = "قائمة الشركات المعتمدة فارغة حالياً.";
        document.getElementById("no-results").style.display = "block";
        return;
    }
    
    companies = [];
    
    // قراءة الأسطر بدءاً من السطر الثاني (تخطي العناوين)
    for (let i = 1; i < lines.length; i++) {
        // نأخذ العمود الأول من كل سطر
        const columns = lines[i].split(",");
        const companyName = columns[0].trim();
        
        if (companyName) {
            companies.push(companyName);
        }
    }
    
    // عرض القائمة وتفعيل البحث
    renderCompanies(companies);
    initTableSearch();
}

// 3. إدارة المظهر (الوضع الداكن / الفاتح)
function initTheme() {
    const themeToggleBtn = document.getElementById("theme-toggle");
    const sunIcon = document.getElementById("theme-icon-sun");
    const moonIcon = document.getElementById("theme-icon-moon");
    
    const savedTheme = localStorage.getItem("theme") || 
                       (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    
    setTheme(savedTheme);
    
    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        setTheme(newTheme);
    });

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        
        if (theme === "dark") {
            sunIcon.style.display = "block";
            moonIcon.style.display = "none";
        } else {
            sunIcon.style.display = "none";
            moonIcon.style.display = "block";
        }
    }
}

// 4. توليد وعرض عناصر القائمة للزوار للقراءة والبحث فقط
function renderCompanies(data) {
    const listContainer = document.getElementById("company-list");
    listContainer.innerHTML = "";
    
    if (data.length === 0) {
        document.getElementById("no-results").style.display = "block";
        return;
    }
    
    document.getElementById("no-results").style.display = "none";
    
    data.forEach(name => {
        const item = document.createElement("div");
        item.className = "company-item";
        item.textContent = name;
        
        listContainer.appendChild(item);
    });
}

// 5. منطق البحث الفوري والفلترة
function initTableSearch() {
    const searchInput = document.getElementById("search-input");
    
    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim().toLowerCase();
        
        const filtered = companies.filter(name => {
            return name.toLowerCase().includes(query);
        });
        
        renderCompanies(filtered);
    });
}
