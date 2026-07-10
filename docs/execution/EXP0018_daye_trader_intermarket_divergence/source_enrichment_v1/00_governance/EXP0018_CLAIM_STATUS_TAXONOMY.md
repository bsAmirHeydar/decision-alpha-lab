# طبقه‌بندی وضعیت ادعاها

| وضعیت | معنی | اجازه ورود به کد |
|---|---|---|
| `canonical` | در Word یا تصمیم معمار صریح و بدون تعارض | بله، پس از phase gate |
| `corroborating` | PDF همان قانون canonical را تأیید می‌کند | به‌عنوان evidence |
| `clarifying_candidate` | جزئیات لازم را پیشنهاد می‌دهد ولی نیازمند تأیید است | خیر |
| `research_candidate` | مفهوم جدید و قابل تست است | فقط research module |
| `conflict` | با منبع بالاتر یا منبع دیگر ناسازگار است | مسدود |
| `quarantined` | ادعای غیرقابل اندازه‌گیری، شخصی یا غیرمهندسی | هرگز در هسته |
| `example_only` | صرفاً مثال تصویری است | فقط test fixture candidate |

هر ادعا باید `claim_id`، منبع، صفحه، وضعیت، اثر احتمالی و test requirement داشته باشد.
