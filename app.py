from flask import Flask, request, jsonify, render_template_string, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
# تفعيل CORS للسماح لصفحة GitHub Pages بإرسال بيانات التتبع دون قيود الأمان للمتصفح
CORS(app) 

DB_NAME = "analytics.db"

# إنشاء قاعدة البيانات والجداول تلقائياً عند تشغيل السيرفر لأول مرة
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ip TEXT,
                user_agent TEXT,
                referer TEXT
            )
        """)
        conn.commit()

# 1. الرابط الرئيسي: يحول الزائر تلقائياً إلى لوحة التحكم بدلاً من إظهار خطأ Not Found
@app.route("/")
def home():
    return redirect("/admin/dashboard")

# 2. الـ API المخفي: يتم استدعاؤه في الخلفية من صفحة أمانة الرياض لتسجيل الزيارة
@app.route("/api/track", methods=["POST"])
def track_view():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO views (timestamp, ip, user_agent, referer) VALUES (?, ?, ?, ?)",
            (timestamp, ip, user_agent, referer)
        )
        conn.commit()
        
    return jsonify({"status": "success"}), 200

# 3. لوحة التحكم السرية: تستعرض الإحصائيات بالتفصيل والوقت الفعلي
@app.route("/admin/dashboard")
def dashboard():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # حساب إجمالي عدد الزيارات
        cursor.execute("SELECT COUNT(*) FROM views")
        total_views = cursor.fetchone()[0]
        
        # حساب عدد الزوار الفريدين بناءً على الـ IP
        cursor.execute("SELECT COUNT(DISTINCT ip) FROM views")
        unique_visitors = cursor.fetchone()[0]
        
        # جلب آخر 10 زيارات مسجلة
        cursor.execute("SELECT timestamp, ip, user_agent FROM views ORDER BY id DESC LIMIT 10")
        recent_views = cursor.fetchall()
        
    # تصميم واجهة لوحة التحكم المتوافقة مع ألوان الهوية الرسمية (الأخضر والذهبي)
    dashboard_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>لوحة تحكم الإحصائيات الخاصة بك</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
        <style>
            body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
            .bg-custom-green { background-color: #005A36; color: white; }
            .text-custom-gold { color: #D4AF37; }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="text-dark fw-bold">📊 نظام الإحصائيات المتقدم المستقل</h2>
                <span class="badge bg-custom-green p-2 fs-6">محدث فورياً</span>
            </div>
            
            <div class="row g-4 mb-5">
                <div class="col-md-6">
                    <div class="card p-4 text-center">
                        <h5 class="text-muted fw-semibold">إجمالي المشاهدات (Pageviews)</h5>
                        <h1 class="display-3 fw-bold text-success">{{ total_views }}</h1>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card p-4 text-center">
                        <h5 class="text-muted fw-semibold">الزوار الفريدون (Unique Visitors)</h5>
                        <h1 class="display-3 fw-bold text-primary">{{ unique_visitors }}</h1>
                    </div>
                </div>
            </div>

            <div class="card p-4">
                <h5 class="mb-4 fw-bold text-dark">📋 سجل آخر 10 زيارات حية</h5>
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>الوقت والتاريخ</th>
                                <th>عنوان IP الخاص بالزائر</th>
                                <th>المتصفح ونظام التشغيل</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for view in recent_views %}
                            <tr>
                                <td class="text-muted">{{ view[0] }}</td>
                                <td><span class="badge bg-secondary px-3 py-2 fs-6">{{ view[1] }}</span></td>
                                <td class="text-truncate text-muted" style="max-width: 400px;" title="{{ view[2] }}">{{ view[2] }}</td>
                            </tr>
                            {% endfor %}
                            {% if not recent_views %}
                            <tr>
                                <td colspan="3" class="text-center text-muted py-4">لا توجد زيارات مسجلة حتى الآن.</td>
                            </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(dashboard_template, total_views=total_views, unique_visitors=unique_visitors, recent_views=recent_views)

if __name__ == "__main__":
    init_db()
    # تشغيل التطبيق محلياً للتجربة (عند الرفع على Render سيتم تجاوزه وتشغيله عبر gunicorn تلقائياً)
    app.run(host="0.0.0.0", port=5000)
