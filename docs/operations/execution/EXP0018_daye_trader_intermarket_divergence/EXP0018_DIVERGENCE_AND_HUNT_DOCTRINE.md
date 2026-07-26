# دکترین هانت و واگرایی Daye

## دو نماد

- Symbol A پیش‌فرض: SPXUSD
- Symbol B پیش‌فرض: NDXUSD

نام واقعی باید input باشد تا suffix/prefix بروکر پشتیبانی شود.

## هانت

- high hunt: `current_high >= reference_high`
- low hunt: `current_low <= reference_low`
- equality لمس محسوب می‌شود.
- close پشت سطح لازم نیست.

## واگرایی یک‌طرفه

برای یک reference pair مشخص:

- فقط A هانت کند و B نکند؛ یا
- فقط B هانت کند و A نکند.

اگر هر دو تا زمان confirmation همان سمت را هانت کرده باشند، آن نوع واگرایی برقرار نیست.

## Hunter و Protected

- Hunter: نمادی که سطح متناظر خودش را هانت کرده است.
- Protected: نمادی که سطح متناظر خودش را هنوز هانت نکرده است.

## جهت

مثال صریح منبع SELL را با high-side توضیح می‌دهد. بنابراین تفسیر پیشنهادی، نه هنوز قطعی:

- high-side one-sided hunt → SELL divergence
- low-side one-sided hunt → BUY divergence

جمله‌ای در منبع این ترتیب را وارونه بیان کرده است. کدنویسی جهت باید تا تأیید متوقف بماند.

## استقلال سیگنال‌ها

اگر در یک کندل چند signal type برقرار باشند، همه باید مستقل ثبت و رسم شوند؛ حتی اگر بعضی BUY و بعضی SELL باشند.
