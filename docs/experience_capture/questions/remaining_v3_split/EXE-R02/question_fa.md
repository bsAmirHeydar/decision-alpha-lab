# EXE-R02 — Broker Validator and Send Gate

چرا مهم است: چون حتی اگر NDS یک intent عالی بسازد، broker ممکن است به خاطر min stop، tick، margin، freeze level یا max lot اجازه اجرا ندهد. این لایه باید جلوی اجرای خراب را بگیرد.

برای پاسخ، حتماً این موارد را روشن کن:
• کدام broker constraints باید حتماً چک شوند؟
• Min stop distance چطور با structural stop مقایسه می‌شود؟
• Tick size و digits چطور normalize می‌شوند؟
• Lot step، min lot و max lot چطور اعمال می‌شوند؟
• Margin کافی نبود، intent veto می‌شود یا حجم adjust می‌شود؟
• Spread چه زمانی باعث veto می‌شود؟
• Freeze level و trade mode چطور لحاظ می‌شوند؟
• Market open/session مهم است؟
• Order rejection handling چطور باشد؟
• چه زمانی adjust مجاز است و چه زمانی veto؟

عکس لازم: خیر. پاسخ متنی کافی است.

خروجی مورد انتظار بعد از پاسخ:
• broker_validation_model_v1.csv
• send_gate_policy_v1.csv
• execution_veto_reason_taxonomy_v1.csv
• order_rejection_handling_v1.csv

پاسخ شما:
