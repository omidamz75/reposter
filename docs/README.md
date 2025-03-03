# ربات ریپوستر تلگرام

ربات مدیریت تبلیغات و ریپوست برای کانال‌های تلگرام

## نصب و راه‌اندازی

1. کلون کردن پروژه:
```bash
git clone https://github.com/yourusername/reposter.git
cd reposter
```

2. ساخت محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
.\venv\Scripts\activate  # Windows
```

3. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4. کپی فایل .env.example به .env و تنظیم متغیرها:
```bash
cp .env.example .env
# ویرایش فایل .env و وارد کردن توکن ربات و سایر تنظیمات
```

5. اجرای ربات:
```bash
python main.py
```

## ساختار پروژه

```
reposter/
├── core/                   # هسته اصلی ربات
│   ├── database.py        # مدیریت دیتابیس
│   └── logger.py          # سیستم لاگینگ
├── modules/               # ماژول‌های ربات
│   ├── users/            # مدیریت کاربران
│   ├── channels/         # مدیریت کانال‌ها
│   └── ads/             # مدیریت تبلیغات
├── tests/                # تست‌ها
├── docs/                 # مستندات
└── main.py              # نقطه شروع برنامه
```

## نحوه مشارکت

لطفاً [راهنمای مشارکت](CONTRIBUTING.md) را مطالعه کنید.

## روند توسعه

جزئیات فازهای توسعه در [مستندات توسعه](DEVELOPMENT.md) موجود است.

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.
