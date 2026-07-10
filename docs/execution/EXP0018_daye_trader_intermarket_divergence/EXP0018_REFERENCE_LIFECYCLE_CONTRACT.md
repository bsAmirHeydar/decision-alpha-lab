# قرارداد چرخه عمر مرجع Daye

## اصل مصرف سطح

سطحی که از آن عبور شده یا sweep/break شده است، نباید بدون قاعده دوباره به‌عنوان reference تازه استفاده شود.

## Protected-based retirement

برای هر reference side:

1. یک نماد Hunter می‌شود.
2. نماد دیگر Protected باقی می‌ماند.
3. تا وقتی Protected سطح خودش را هانت نکرده، reference ساختاری هنوز زنده تلقی می‌شود.
4. به‌محض اینکه Protected همان high/low را هانت کند، reference side بازنشسته می‌شود.
5. reference بازنشسته‌شده دیگر سیگنال جدید نمی‌سازد.

## First-sweep statement

منبع همچنین می‌گوید اگر high روز قبل چند بار sweep شد، فقط بار اول مهم است.

## تعارض نیازمند تصمیم

دو تفسیر ممکن وجود دارد:

- **Strict one-shot:** هر reference فقط یک سیگنال قطعی می‌سازد.
- **Protected-survival:** تا زمانی که Protected زنده است، مراحل جدید می‌توانند دوباره از همان reference استفاده کنند.

این تعارض قبل از کدنویسی باید حل شود. پیشنهاد مهندسی: دو policy صریح با یک policy پیش‌فرض، نه منطق مبهم.

## کلید lifecycle پیشنهادی

`signal_type + trading_period_id + reference_period_id + side + hunter_symbol + protected_symbol`
