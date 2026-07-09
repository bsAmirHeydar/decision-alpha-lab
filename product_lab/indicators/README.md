# Indicators

هر پوشه داخل این بخش یک اندیکاتور محصولی مستقل است. اندیکاتورهای تحقیقاتی یا ناقص نباید مستقیم اینجا قرار بگیرند، مگر اینکه هدف آن‌ها محصول‌سازی باشد.

## ساخت اندیکاتور جدید

از روت پروژه:

```powershell
.\product_lab\scripts\New-ProductLabItem.ps1 -Type indicator -Slug "my-indicator" -Title "My Indicator"
```

## ساختار هر اندیکاتور

```text
indicator-slug/
├── README.md
├── spec/
│   ├── PRODUCT_SPEC.md
│   ├── USER_GUIDE.md
│   ├── VALIDATION_PLAN.md
│   └── CHANGELOG.md
├── mql5/
├── screenshots/
└── release/
```

## قانون ورود به Beta

قبل از Beta باید این فایل‌ها پر شده باشند:

- `PRODUCT_SPEC.md`
- `USER_GUIDE.md`
- `VALIDATION_PLAN.md`
- `CHANGELOG.md`
