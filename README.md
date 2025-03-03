# ...existing content...

## ساختار پروژه
```
reposter/
├── core/                   # هسته اصلی
│   ├── database.py        # مدیریت دیتابیس
│   └── logger.py          # لاگینگ مرکزی
├── modules/
│   └── users/             # ماژول مدیریت کاربران
│       ├── models.py      # مدل‌های دیتابیس
│       ├── services.py    # منطق کسب‌وکار
│       ├── handlers.py    # هندلرهای تلگرام
│       └── logs/          # لاگ‌های اختصاصی
├── tests/                 # تست‌ها
└── data/                  # دیتابیس و لاگ‌ها
```

## راه‌اندازی محیط توسعه
1. نصب پیش‌نیازها:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. تنظیمات VSCode:
- نصب افزونه‌های Python و Pylint
- باز کردن پوشه پروژه در VSCode
- تنظیمات اتوماتیک اعمال می‌شود

## برنچ‌های اصلی
- `main`: نسخه پایدار
- `feature/user-management`: مدیریت کاربران
  - ثبت‌نام کاربران
  - پنل مدیریت ادمین
  - لیست و فیلتر کاربران

## لاگ‌ها
- لاگ‌های عمومی: `data/logs/bot.log`
- لاگ‌های کاربران: `data/logs/users.log`
