# DST-R03 — Destination Repricing and Completion

چرا مهم است: چون مقصدها با حرکت بازار ثابت نمی‌مانند. بعضی مصرف می‌شوند، بعضی repriced می‌شوند، بعضی وزن می‌گیرند یا می‌میرند. بدون lifecycle مقصد، optionality و position management ناقص می‌ماند.

برای پاسخ، حتماً این موارد را روشن کن:
• مقصد چه زمانی consumed می‌شود؟
• تاچ مقصد کافی است یا باید قیمت از آن عبور کند؟
• اگر مقصد اول خورده شد، مقصدهای بعدی چگونه وزن می‌گیرند؟
• اگر مقصد جدید ساخته شد، آیا به لیست مقصدها اضافه می‌شود؟
• اگر مقصد قبلی دیگر optionality ندارد، حذف می‌شود یا historical می‌ماند؟
• مقصدهای opposite direction با position فعال چه می‌کنند؟
• اگر مقصد نزدیک شود، position کاهش می‌یابد یا فقط optionality score پایین می‌آید؟
• مقصد با سناریو می‌میرد یا lifecycle مستقل دارد؟
• مقصدهای parent و child چطور به هم وصل می‌شوند؟
• خروجی state machine مقصد چیست؟

عکس لازم: اختیاری.

خروجی مورد انتظار بعد از پاسخ:
• destination_state_machine_v1.csv
• destination_repricing_policy_v1.csv
• destination_completion_policy_v1.csv
• destination_consumption_model_v1.csv

پاسخ شما:
