# EXE-R01 — ExecutionIntent Contract Finalization

چرا مهم است: چون سیستم نباید مستقیم order بفرستد. NDS باید فقط ExecutionIntent بسازد و validator تصمیم بگیرد که قابل ارسال هست یا نه. پس قرارداد intent باید دقیق باشد.

برای پاسخ، حتماً این موارد را روشن کن:
• حداقل فیلدهای اجباری ExecutionIntent چیست؟
• scenario_id، zone_id، entry_extreme_id، node_id و destination_id چطور به هم وصل می‌شوند؟
• Structural price و adjusted price جدا ذخیره شوند؟
• Spread adjustment کجا ثبت شود؟
• Stop buffer و دلیلش کجا ثبت شود؟
• Risk budget و volume چطور ثبت شود؟
• Split orders داخل همان intent باشند یا child intents؟
• Cancel/replace/missed conditions داخل intent باشند؟
• Intent بدون broker validation قابل اجرا نیست؟
• چه چیزی intent را unsafe می‌کند؟

عکس لازم: خیر. پاسخ متنی کافی است.

خروجی مورد انتظار بعد از پاسخ:
• execution_intent_contract_v1.csv
• execution_intent_lineage_v1.csv
• structural_vs_adjusted_price_model_v1.csv
• intent_safety_flags_v1.csv

پاسخ شما:
