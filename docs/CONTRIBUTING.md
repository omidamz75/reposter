# راهنمای مشارکت در پروژه

## گردش کار گیت

### شروع کار با قابلیت جدید
1. به‌روزرسانی برنچ main:
```bash
git checkout main
git pull origin main
```

2. ایجاد برنچ جدید:
```bash
git checkout -b feature/نام-قابلیت
```

### توسعه قابلیت
1. کد را با استانداردهای پروژه بنویسید
2. تست‌ها را بنویسید
3. تغییرات را کامیت کنید:
```bash
git add .
git commit -m "توضیح تغییرات"
```

### تست و بررسی
1. اجرای تست‌ها:
```bash
pytest tests/
```

2. بررسی کیفیت کد:
```bash
black .
```

### ادغام تغییرات
1. به‌روزرسانی برنچ خود با main:
```bash
git checkout main
git pull origin main
git checkout feature/نام-قابلیت
git merge main
```

2. رفع تداخل‌ها (در صورت وجود)
3. اجرای مجدد تست‌ها
4. ادغام با main:
```bash
git checkout main
git merge feature/نام-قابلیت
git push origin main
```

## استانداردهای کدنویسی
- استفاده از Type Hints
- نوشتن docstring برای توابع
- رعایت PEP 8
- نوشتن تست برای هر قابلیت
- استفاده از black برای فرمت کد

## ساختار برنچ‌ها
- `main`: نسخه پایدار
- `feature/*`: قابلیت‌های جدید
- `bugfix/*`: رفع باگ‌ها
- `hotfix/*`: رفع مشکلات حیاتی

## مستندسازی
- به‌روزرسانی README.md
- مستندسازی تغییرات API
- به‌روزرسانی CHANGELOG.md
