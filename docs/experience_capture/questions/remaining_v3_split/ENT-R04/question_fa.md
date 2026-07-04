# ENT-R04 — After Fill: Scenario-to-Position Transition

چرا مهم است: چون وقتی limit پر شد، سیستم از تحلیل و intent وارد position واقعی می‌شود. باید معلوم باشد بعد از fill، سناریو هنوز زنده است، تبدیل به position thread می‌شود، یا وارد مدیریت مستقل معامله می‌شود.

برای پاسخ، حتماً این موارد را روشن کن:
• بعد از fill، ScenarioThread همچنان زنده می‌ماند یا به PositionThread تبدیل می‌شود؟
• اگر parent scenario بعد از ورود ضعیف شد، position چه واکنشی دارد؟
• اگر سناریوی مخالف بعد از ورود قوی‌تر شد، position کاهش پیدا می‌کند، hedge می‌شود، یا فقط با stop/TP مدیریت می‌شود؟
• استاپ بعد از fill ثابت می‌ماند یا با ساختار جدید می‌تواند جابه‌جا شود؟
• اگر مقصد اول خورده شد، position partially completed می‌شود یا سناریو همچنان زنده است؟
• خروج پله‌ای جزو scenario است یا position management؟
• اگر چند entry داخل یک zone داریم، بعد از fill جدا مدیریت می‌شوند یا یک position bucket می‌شوند؟
• اگر max lot split شده بود، معامله‌ها جدا هستند یا یک logical position واحد؟
• چه چیزی position را کامل می‌کند: TP کامل، invalidation، پایان مقصدها، یا خروج دستی/سیستمی؟
• خروجی نهایی چه stateهایی داشته باشد؟

عکس لازم: اختیاری. اگر نمونه چند fill یا خروج پله‌ای داری، عکس کمک می‌کند.

خروجی مورد انتظار بعد از پاسخ:
• scenario_to_position_transition_v1.csv
• position_thread_model_v1.csv
• partial_exit_state_v1.csv
• split_order_position_aggregation_v1.csv

پاسخ شما:
