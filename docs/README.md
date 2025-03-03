# ربات ریپوستر تلگرام

ربات مدیریت تبلیغات و ریپوست برای کانال‌های تلگرام

## مستندات

- [راهنمای توسعه](DEVELOPMENT.md)
- [راهنمای مشارکت](CONTRIBUTING.md)
- [معماری پروژه](ARCHITECTURE.md)

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

4. تنظیم متغیرهای محیطی:
```bash
cp .env.example .env
# ویرایش فایل .env
```

5. اجرای ربات:
```bash
python main.py
```

## کتابخانه‌های اصلی

- **python-telegram-bot**: کتابخانه رسمی تلگرام با پشتیبانی از async/await
- **SQLAlchemy**: ORM قدرتمند برای مدیریت دیتابیس
- **python-dotenv**: مدیریت متغیرهای محیطی
- **loguru**: سیستم لاگینگ پیشرفته
- **pytest**: فریم‌ورک تست‌نویسی
- **black**: فرمت‌کننده کد پایتون
