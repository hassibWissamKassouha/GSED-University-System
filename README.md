# 🎓 نظام إدارة شؤون الطلاب والدراسات العليا (GSED Uni)

هذا المشروع هو النظام الخلفي (Backend) لإدارة العمليات الجامعية، مصمم باستخدام **Django** و **Django Rest Framework** مع قاعدة بيانات **PostgreSQL**. يوفر النظام بيئة متكاملة لإدارة المستخدمين، الطلاب، الأستاذة، العلامات، والمناقشات العلمية.

## 🚀 كيفية تشغيل المشروع محلياً

اتبع الخطوات التالية لتشغيل السيرفر على جهازك:

1. **تحميل المشروع:**
   ```bash
   git clone [رابط_المستودع_الخاص_بك]
   cd Uni
إنشاء بيئة افتراضية وتفعيلها:

Bash
python -m venv venv
# لنظام ويندوز:
venv\Scripts\activate
تثبيت المكتبات المطلوبة:

Bash
pip install -r requirements.txt
تحديث قاعدة البيانات:

Bash
python manage.py migrate
تشغيل السيرفر:

Bash
python manage.py runserver
🛠️ هيكلية البيانات (16 جدولاً)
يحتوي النظام على الجداول الأساسية التالية المسجلة في لوحة التحكم:

الهوية: GlobalUser, Role, Permission.

الأكاديميا: Department, Student, Professor, Course.

النتائج: Grade, ExamSession, ExamHallAllocation.

الدراسات العليا: Thesis, Seminar.

الإدارة: Decree, UserDecree, DocumentRequest.

🔌 توثيق الـ API (للمطورين - Frontend)
لقد تم تفعيل نظام CORS للسماح بربط تطبيقات الـ Frontend الخارجية.

1. تسجيل الدخول (Login)
Endpoint: /api/login/

Method: POST

Body (JSON):

JSON
{
    "id": 20201010,
    "password": "your_password"
}
Success Response (200 OK):

JSON
{
    "token": "9944b09199c62bcf9418ad846dd0e4...",
    "user_id": 20201010,
    "role": "Student",
    "name": "Ahmad Ali"
}
2. طريقة المصادقة (Authentication)
للوصول إلى أي API محمي، يجب إرسال التوكن في الـ Header كالتالي:
Authorization: Token [your_token_here]

📝 ملاحظات إضافية
يتم إضافة المستخدمين الجدد وتعيين الأدوار لهم حصراً من خلال Django Admin على الرابط: /admin/.

تم إعداد النظام لرفض دخول الحسابات المقفلة isLocked.


---

### ماذا تفعل الآن؟
1. افتح ملف `README.md` في VS Code.
2. احذف أي نص قديم فيه.
3. الصق النص أعلاه.
4. **احفظ الملف.**
5. نفذ الأوامر التالية في التيرمينال لإرساله لـ GitHub:

```bash
git add README.md
git commit -m "Update README with full API documentation and instructions"
git push
