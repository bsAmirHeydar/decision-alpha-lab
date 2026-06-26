# EXP0016 Astro Meta Learner — Professional Operating Manual

این ماژول لایه‌ی یادگیری حرفه‌ای روی سیستم آسترولوژی مکانیکی پروژه است. هدفش این نیست که از قبل بگوید «مشتری یعنی خرید» یا «زحل یعنی فروش». هدف این است که از داده‌ی مکانیکی آسترولوژی و نتیجه‌ی واقعی بازار یاد بگیرد:

```text
Astro state at candle t
+
Market outcome after candle t
=
Learned astro logic
```

یعنی مدل خودش یاد می‌گیرد که یک ترکیب آسترولوژیک چه زمانی واقعاً جهت می‌دهد، چه زمانی فقط نوسان می‌دهد، چه زمانی trap می‌سازد، و چه زمانی مسیر را تمیز یا کثیف می‌کند.

---

## 1. خروجی نهایی این سیستم چیست؟

بعد از اجرای پروتکل، سیستم این‌ها را می‌سازد:

```text
1. دیتاست یادگیری causal
2. اکسل audit دیتاست
3. چند مدل جدا برای direction / clean path / spike / trap
4. تست chronological train/test
5. تست walk-forward با embargo
6. model card برای هر مدل
7. memory دائمی از چیزهایی که مدل یاد گرفته
8. knowledge pack قابل انتقال برای استفاده در جاهای دیگر
9. prediction فایل برای دیتای خارج از train
```

مسیر اصلی خروجی‌ها:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml\
```

Memory اصلی:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml\memory\NAS100\M1\
```

Protocol runs:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml\protocol_runs\NAS100\M1\
```

---

## 2. معماری حرفه‌ای

```text
[Astro Feature CSV]
        |
        v
[Price OHLC CSV]
        |
        v
[Dataset Builder]
        |
        +--> labels: direction / clean long / clean short / spike / bull trap / bear trap
        |
        v
[Dataset Audit]
        |
        +--> missing values
        +--> time gaps
        +--> label distributions
        +--> leakage-name candidates
        +--> constant columns
        |
        v
[Model Suite]
        |
        +--> direction model
        +--> clean long model
        +--> clean short model
        +--> spike model
        +--> bull-trap model
        +--> bear-trap model
        |
        v
[Chronological Evaluation]
        |
        v
[Walk-forward Evaluation]
        |
        v
[Model Card + Feature Importance]
        |
        v
[Astro Memory]
        |
        v
[Knowledge Pack]
```

اصل حیاتی:

```text
هیچ feature در کندل t نباید از آینده خبر داشته باشد.
Outcome فقط بعد از t ساخته می‌شود.
Train/Test باید زمانی باشد، نه random.
```

---

## 3. فایل‌های اضافه‌شده

```text
tools/astro_ml/
  astro_ml_core.py
  build_astro_ml_dataset.py
  astro_ml_audit_dataset.py
  train_astro_meta_learner.py
  evaluate_walk_forward.py
  explain_astro_model.py
  make_astro_model_card.py
  predict_with_astro_memory.py
  query_astro_memory.py
  export_astro_knowledge_pack.py
  run_astro_ml_protocol.py

  build_astro_ml_dataset_common.ps1
  audit_astro_ml_dataset_common.ps1
  train_astro_meta_learner_common.ps1
  evaluate_walk_forward_common.ps1
  explain_astro_model_common.ps1
  make_astro_model_card_common.ps1
  predict_with_astro_memory_common.ps1
  query_astro_memory_common.ps1
  export_astro_knowledge_pack_common.ps1
  run_astro_ml_protocol_common.ps1

  configs/NAS100_M1_professional_protocol.json

mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

مهم‌ترین فایل برای استفاده راحت:

```text
tools/astro_ml/run_astro_ml_protocol_common.ps1
```

این یک دستور تقریباً همه‌چیز را انجام می‌دهد.

---

## 4. نصب اولیه فقط یک بار

از روت پروژه:

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

python -m pip install -r .\tools\astro_ml\requirements.txt
```

اگر خطای `scikit-learn` یا `openpyxl` گرفتی:

```powershell
python -m pip install pandas numpy scikit-learn joblib openpyxl
```

---

## 5. ورودی‌های لازم

برای یادگیری واقعی، دو فایل لازم است:

### 5.1 فایل آسترولوژی مکانیکی

مثلاً:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv
```

این فایل featureهای آسترولوژیک کندل‌به‌کندل را دارد.

### 5.2 فایل قیمت OHLC

این را با اسکریپت متاتریدر می‌گیریم:

```text
mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

در MetaEditor کامپایل کن و از Navigator اجرا کن.

برای نمونه NAS100 M1:

```text
InpSymbol         = NAS100
InpTimeframe      = PERIOD_M1
InpFrom           = 2026.06.22 00:00
InpTo             = 2026.06.27 23:59
InpOutputName     = astro_ml_prices_NAS100_M1_20260622_to_now.csv
InpUseCommonFiles = true
```

خروجی:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml_prices_NAS100_M1_20260622_to_now.csv
```

---

# 6. ساده‌ترین پروتکل استفاده — فقط همین را بزن

از روت پروژه:

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"
```

بعد:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset professional `
  -Horizons "30,60,120" `
  -OpenAfter
```

این دستور به‌صورت خودکار انجام می‌دهد:

```text
1. ساخت دیتاست
2. audit دیتاست
3. ترین مدل‌های اصلی
4. ساخت model card
5. ذخیره memory
6. ساخت knowledge pack
7. بازکردن گزارش نهایی
```

برای دیتای چندروزه فعلی، اگر فقط می‌خواهی sanity سریع بگیری:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

---

# 7. پروتکل حرفه‌ای با walk-forward

برای دیتای چندماهه یا چندساله:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_2022_to_2026_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -OpenAfter
```

برای دیتای کوتاه چندروزه، walk-forward کوچک‌تر:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 2 `
  -TestDays 1 `
  -StepDays 1 `
  -EmbargoBars 120 `
  -OpenAfter
```

اما نتیجه جدی از دیتای چندروزه نگیر. این فقط برای تست سلامت pipeline است.

---

## 8. Targetهایی که مدل یاد می‌گیرد

اگر `-Preset professional` بگذاری، پیش‌فرض این‌ها train می‌شوند:

```text
label_direction_30
label_direction_60
label_direction_120
label_clean_long_60
label_clean_short_60
label_spike_60
label_bull_trap_60
label_bear_trap_60
```

معنی‌ها:

```text
label_direction_60:
  در ۶۰ کندل بعد، بازار UP / DOWN / FLAT شد؟

label_clean_long_60:
  مسیر لانگ در ۶۰ کندل بعد تمیز بود یا نه؟

label_clean_short_60:
  مسیر شورت در ۶۰ کندل بعد تمیز بود یا نه؟

label_spike_60:
  نوسان/اسپایک معنی‌دار داشت یا نه؟

label_bull_trap_60:
  اول بالا را نشان داد ولی بعد برگشت و لانگ را trap کرد؟

label_bear_trap_60:
  اول پایین را نشان داد ولی بعد برگشت و شورت را trap کرد؟
```

برای اینکه فقط جهت را train کنی:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset direction_only `
  -Horizons "30,60,120" `
  -OpenAfter
```

برای target دستی:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Targets "label_direction_60,label_bull_trap_60,label_clean_short_60" `
  -OpenAfter
```

---

## 9. Memory دقیقاً چطور کار می‌کند؟

هر train یک run جدا می‌سازد:

```text
Common\Files\astro_ml\memory\NAS100\M1\runs\<RUN_ID>\
```

داخل هر run:

```text
model.joblib
metadata.json
metrics.json
feature_importance.csv
test_predictions.csv
training_report.xlsx
MODEL_CARD.md
model_card.json
model_card.xlsx
knowledge_base.json
```

فایل‌های تجمعی memory:

```text
memory_index.csv
knowledge_memory.jsonl
latest_run.txt
astro_knowledge_pack_NAS100_M1.json
astro_knowledge_pack_NAS100_M1.md
```

`memory_index.csv` خلاصه همه runها را نگه می‌دارد.

`knowledge_memory.jsonl` درس‌هایی است که مدل از feature importance و نتیجه‌ها استخراج کرده.

`knowledge_pack` کل این حافظه را تبدیل می‌کند به یک بسته قابل انتقال، تا بعداً برای مدل‌های دیگر یا دارایی‌های دیگر استفاده شود.

---

## 10. پرسیدن از memory

برای دیدن حافظه:

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

برای جست‌وجوی Saturn:

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -Contains saturn `
  -OpenAfter
```

برای trap:

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -Contains trap `
  -OpenAfter
```

برای ساخت knowledge pack دستی:

```powershell
.\tools\astro_ml\export_astro_knowledge_pack_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

---

## 11. استفاده روی دیتای خارج از Train

فرض کن مدل را روی 2022 تا 2025 train کرده‌ای. حالا 2026 را می‌خواهی تست کنی.

اول برای 2026 دیتاست بساز:

```powershell
.\tools\astro_ml\build_astro_ml_dataset_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_2026_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Horizons "30,60,120" `
  -OutName "astro_ml_dataset_NAS100_M1_2026_oos.csv" `
  -OpenAfter
```

بعد آخرین run را پیدا کن:

```powershell
$RunId = Get-Content "$env:APPDATA\MetaQuotes\Terminal\Common\Files\astro_ml\memory\NAS100\M1\latest_run.txt" -Raw
$RunId = $RunId.Trim()
$RunDir = "astro_ml\memory\NAS100\M1\runs\$RunId"
```

بعد prediction بگیر:

```powershell
.\tools\astro_ml\predict_with_astro_memory_common.ps1 `
  -RunDir $RunDir `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_2026_oos.csv" `
  -OutCsv "astro_ml\reports\NAS100\M1\NAS100_M1_2026_oos_predictions.csv" `
  -OpenAfter
```

---

## 12. مدل کی قابل قبول است؟

قبولی فقط با accuracy نیست. معیار حرفه‌ای:

```text
1. balanced_accuracy از baseline بهتر باشد.
2. walk-forward خراب نشود.
3. فقط روی یک هفته یا یک ماه خاص کار نکند.
4. feature importance معنادار باشد.
5. leakage-name candidates وارد feature set نشده باشند.
6. روی out-of-sample دست‌نخورده هم رفتار خوب بماند.
7. خروجی اقتصادی هم با MAE/MFE و هزینه‌ها قابل دفاع باشد.
```

حداقل وضعیت:

```text
balanced_accuracy < 0.52  => فعلاً رد / research only
0.52 تا 0.55              => ضعیف، نیاز به دیتای بیشتر و audit
0.55 تا 0.60              => candidate برای تست بیشتر
0.60 به بالا              => جدی‌تر، ولی باز هم باید walk-forward و OOS بماند
```

برای trap/spike چون class imbalance زیاد است، فقط accuracy کافی نیست. باید `balanced_accuracy` و `f1_macro` را ببینی.

---

## 13. چرا این از rule-based قبلی حرفه‌ای‌تر است؟

Rule-based قبلی می‌گفت:

```text
Jupiter support زیاد است => BUY
Saturn pressure زیاد است => SELL
```

اما این مدل یاد می‌گیرد:

```text
Jupiter support + low Saturn pressure + clean timing => احتمال long continuation
Jupiter support + exhaustion + Mars/Saturn conflict => احتمال bull trap
Moon/Mars pressure => شاید direction ندهد، اما spike بدهد
Saturn pressure + clean short path => sell candidate
Venus/Jupiter فقط participation بدهد، نه direction
```

پس خروجی نهایی دیگر یک سیگنال خام نیست. یک تفکیک چندلایه است:

```text
direction
path cleanliness
spike/hunt
trap/reversal
confidence
```

---

## 14. پروتکل پیشنهادی برای پروژه اصلی

برای نتیجه جدی روی NAS100:

### مرحله 1 — دیتای بزرگ

```text
NAS100 M1 یا M5 از 2022 تا 2026
```

### مرحله 2 — ساخت Astro CSV چندساله

با ابزارهای astro feature builder فعلی پروژه.

### مرحله 3 — Export قیمت از MT5

با:

```text
mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

### مرحله 4 — پروتکل professional با walk-forward

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_2022_to_2026_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -OpenAfter
```

### مرحله 5 — خواندن گزارش‌ها

اول این را باز کن:

```text
protocol_report.xlsx
```

بعد برای هر مدل:

```text
MODEL_CARD.md
training_report.xlsx
feature_importance.csv
```

بعد memory:

```text
astro_knowledge_pack_NAS100_M1.md
```

---

## 15. تفسیر خروجی‌ها

### اگر direction مدل خوب است

یعنی آسترولوژی در آن horizon جهت داده.

### اگر direction ضعیف است ولی spike خوب است

یعنی آسترولوژی بیشتر برای نوسان/هانت مفید است، نه جهت.

### اگر clean_short خوب است ولی direction متوسط است

یعنی شاید جهت خام سخت است، اما مسیرهای شورت تمیز قابل تشخیص‌اند.

### اگر bull_trap خوب است

یعنی مشکل BUY-only فعلی قابل حل است؛ مدل یاد گرفته کدام حالت‌های ظاهراً bullish در واقع trap هستند.

### اگر همه ضعیف‌اند

یعنی در آن فرم feature/label، آسترولوژی edge نداده یا دیتای کافی نیست.

---

## 16. نکته حیاتی درباره دیتای کوتاه فعلی

فایل چندروزه‌ی فعلی برای sanity خوب است، نه نتیجه نهایی.

```text
چند روز دیتا = تست pipeline
چند ماه دیتا = تحقیق اولیه
چند سال دیتا = نتیجه قابل اتکا
```

اگر روی چند روز نتیجه خیلی خوب شد، به آن اعتماد نکن. باید out-of-sample و walk-forward بزرگ بماند.

---

## 17. چک‌لیست سریع اجرا

```text
[ ] astro CSV آماده است
[ ] price CSV از MT5 export شده
[ ] pip requirements نصب شده
[ ] sanity protocol اجرا شده
[ ] dataset audit بررسی شده
[ ] professional protocol اجرا شده
[ ] model cards خوانده شده
[ ] knowledge pack ساخته شده
[ ] walk-forward روی دیتای بزرگ اجرا شده
[ ] OOS untouched تست شده
```

---

## 18. دستورهای اصلی که باید حفظ کنی

### نصب

```powershell
python -m pip install -r .\tools\astro_ml\requirements.txt
```

### اجرای سریع

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset sanity `
  -OpenAfter
```

### اجرای کامل

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_2022_to_2026_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -OpenAfter
```

### پرسیدن از حافظه

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -Contains trap `
  -OpenAfter
```

### ساخت knowledge pack

```powershell
.\tools\astro_ml\export_astro_knowledge_pack_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

---

## 19. تعریف موفقیت این فرضیه

EXP0016 موفق است اگر بتواند یکی از این‌ها را out-of-sample نشان دهد:

```text
1. direction بهتر از baseline
2. spike/hunt بهتر از baseline
3. clean path بهتر از baseline
4. trap detection بهتر از baseline
5. learned rules قابل فهم و پایدار در walk-forward
```

اگر فقط ruleهای خوشگل بسازد ولی OOS خراب شود، رد است.

---

## 20. قرارداد نهایی

این ماژول قرار نیست کورکورانه buy/sell بدهد. قرار است بفهمد:

```text
آسترولوژی مکانیکی برای این دارایی دقیقاً چه چیزی را بهتر توضیح می‌دهد؟
جهت؟
مسیر تمیز؟
نوسان؟
trap؟
زمان‌بندی خروج؟
```

بعد از فهمیدن، می‌توانیم دانش را به اکسپرت‌های اجرایی منتقل کنیم.

---

# V2: Human-Learning Protocol

این نسخه برای همان چیزی ساخته شده که در پروژه می‌خواهیم: مدل فقط یک classifier عددی نباشد؛ مثل یک پژوهشگر انسانی، شرایط را ببیند، تجربه ذخیره کند، الگوهای ضعیف را رد کند، و فقط دانشی را قبول کند که در تست زمانی هم دوام آورده باشد.

## هدف V2

قرارداد V2 این است:

```text
1. قیمت را خودش از MT5 بگیرد.
2. دیتای آسترو را اگر موجود بود از آرشیو بردارد.
3. اگر موجود نبود، خودش با natal درست بسازد.
4. دیتاست causal بسازد: feature در t، outcome بعد از t.
5. مدل‌های قابل تفسیر train کند.
6. cognitive memory بسازد.
7. هر rule را با شک و ضد-overfit بررسی کند.
8. فقط الگوهایی را قبول کند که support و OOS lift و stability داشته باشند.
```

## ساده‌ترین دستور کامل

از روت پروژه:

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

python -m pip install -r .\tools\astro_ml\requirements.txt

.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

این دستور خودش این کارها را انجام می‌دهد:

```text
MT5 -> price CSV
Archive/Builder -> astro CSV
Astro + Price -> ML dataset
Dataset -> audit
Dataset -> train model suite
Dataset -> cognitive memory
Memory -> skeptical rules + case memory + concept memory
```

## دستور حرفه‌ای چندماهه/چندساله

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -CognitiveMinSupport 300 `
  -CognitiveMinLift 1.10 `
  -CognitiveMaxGap 0.15 `
  -OpenAfter
```

برای دیتای چندروزه، `CognitiveMinSupport` را کوچک بگذار. برای دیتای چندساله، بزرگ‌تر بگذار تا مدل الگوهای تصادفی را قبول نکند.

## اگر نمی‌خواهی از MT5 قیمت بگیرد

اگر price csv را قبلاً داری:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -PriceCsv "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -SkipMt5Fetch `
  -Preset sanity `
  -OpenAfter
```

## اگر می‌خواهی حتماً Astro را از صفر بسازد

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -ForceBuildAstro `
  -BrokerGmtOffsetHours 3 `
  -Preset sanity `
  -OpenAfter
```

برای NAS100، natal پیش‌فرض این است:

```text
1985-01-31 09:30 New York
label = nasdaq100_index_1985_ny_open
lat/lon = New York
UTC offset = -5
```

## خروجی‌ها کجا می‌روند؟

### پروتکل اصلی

```text
Common\Files\astro_ml\human_learning_protocols\NAS100\M1\<RUN_ID>\
```

داخلش:

```text
HUMAN_LEARNING_REPORT.md
human_learning_manifest.json
```

### پروتکل ML کلاسیک

```text
Common\Files\astro_ml\protocol_runs\NAS100\M1\<RUN_ID>\
```

داخلش:

```text
PROTOCOL_REPORT.md
protocol_report.xlsx
protocol_manifest.json
```

### مموری مدل‌ها

```text
Common\Files\astro_ml\memory\NAS100\M1\runs\<RUN_ID>\
```

داخلش:

```text
model.joblib
metrics.json
feature_importance.csv
model_card.md
test_predictions.csv
knowledge_base.json
```

### مموری شناختی/انسانی

```text
Common\Files\astro_ml\cognitive_memory\NAS100\M1\<RUN_ID>\
```

داخلش:

```text
COGNITIVE_MEMORY_REPORT.md
cognitive_memory_report.xlsx
skeptical_rules.csv
case_memory.csv
concept_memory.json
concept_memory.jsonl
```

## cognitive memory دقیقاً چیست؟

این بخش تلاش می‌کند مثل یک انسان حرفه‌ای یاد بگیرد، نه مثل یک مدل خام.

### 1. concept families

فیچرها را به خانواده‌های مفهومی تبدیل می‌کند:

```text
saturn_pressure
mars_impulse
jupiter_expansion
venus_value
moon_timing
mercury_information
pluto_pressure
natal_activation
path_quality
macro_context
timing
```

### 2. context signature

برای هر کندل یک امضای زمینه‌ای می‌سازد، مثل:

```text
saturn_pressure=high | jupiter_expansion=low | moon_timing=mid | path_quality=very_low
```

این باعث می‌شود مدل فقط عدد خام نبیند؛ حالت/زمینه ببیند.

### 3. skeptical rules

برای هر target مثل `label_direction_60` یا `label_bull_trap_60`، هزاران قانون احتمالی می‌سازد؛ اما هیچ‌کدام را سریع قبول نمی‌کند.

یک قانون فقط وقتی accepted می‌شود که:

```text
train support کافی داشته باشد
OOS/test support کافی داشته باشد
train lift مثبت باشد
test lift هم مثبت بماند
train/test gap زیاد نباشد
```

اگر این شرط‌ها را نداشته باشد، می‌رود در rejected و دلیل ردش هم نوشته می‌شود:

```text
low_train_support
low_test_support
weak_train_lift
no_oos_lift
unstable_train_test_gap
```

این دقیقاً ضد overfit است.

### 4. case memory

نمونه‌های واقعی را ذخیره می‌کند:

```text
time
cognitive_signature
outcomes
top astro features
```

بعداً می‌توانیم مرحله بعدی را بسازیم که بگوید:

```text
وضعیت امروز شبیه ۴۷ کیس تاریخی است.
در ۶۲٪ آن‌ها DOWN شده.
در ۷۰٪ آن‌ها bull trap رخ داده.
```

## چطور گزارش را بخوانی؟

اول این فایل را باز کن:

```text
COGNITIVE_MEMORY_REPORT.md
```

اگر نوشته:

```text
No accepted rules yet
```

این شکست نیست. یعنی سیستم حاضر نشده با دیتای کم، الگوی الکی قبول کند.

اگر accepted rule داشت، در `skeptical_rules.csv` این ستون‌ها مهم‌اند:

```text
condition
target
label
train_support
test_support
train_lift
test_lift
stability_gap
skepticism_status
rejection_reasons
```

قانون خوب این است:

```text
skepticism_status = accepted
test_lift > 1.10
test_support کافی
stability_gap پایین
```

## چرا این شبیه یادگیری انسان است؟

چون سه لایه دارد:

```text
1. تجربه خام: case_memory
2. مفهوم‌سازی: concept families + context signatures
3. شک و داوری: skeptical_rules با OOS evidence
```

یعنی هر چیزی که دیده را باور نمی‌کند. اول می‌پرسد:

```text
آیا این الگو نمونه کافی دارد؟
آیا فقط در train بوده یا در آینده هم مانده؟
آیا gap زیاد است؟
آیا بهتر از baseline است؟
```

## مسیر بعدی برای چند لول حرفه‌ای‌تر

V2 پایه انسانی/شناختی است. بعد از اینکه روی دیتای واقعی اجرا شد، مرحله بعد می‌تواند این‌ها باشد:

```text
1. Similar-case retrieval
2. calibrated ensemble
3. event-based astro learner
4. sequence learner
5. transformer/temporal CNN فقط بعد از اثبات edge کلاسیک
6. rule-to-MQL exporter
7. live cognitive astro dashboard
```

اصل مهم:

```text
اول باید ثابت شود یک target مثل trap یا clean_path در OOS بهتر از baseline است.
بعد deep learning ارزش دارد.
```

اگر از اول برویم deep، فقط overfit قشنگ‌تر می‌سازیم.


## Self-Healing Data Protocol

From this version onward, the human-learning runner is data-self-healing. You do **not** need to manually prepare Excel/CSV price files before running it.

You only provide:

```powershell
-Asset NAS100
-Symbol NAS100
-Timeframe M1
-From "2026-06-22 00:00"
-To "2026-06-27 23:59"
```

The runner then does the following in order:

1. Checks whether a usable price CSV already exists in `Common\Files` or `Common\Files\astro_ml\prices\<SYMBOL>\<TF>`.
2. If price data is missing or unusable, it fetches candles directly from the local MetaTrader 5 terminal through the Python `MetaTrader5` package.
3. Checks whether a usable astro feature CSV already exists in `Common\Files`, `astro_archive`, or `astro/features`.
4. If astro data is missing or does not cover the requested range, it calls the project astro feature builder and creates a deterministic astro CSV using the asset natal defaults.
5. Builds the causal ML dataset.
6. Audits the dataset.
7. Trains the configured models.
8. Builds skeptical cognitive memory and rejects weak/unstable patterns.

### One-command NAS100 example

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

### Force refresh everything

Use this when you want to ignore old files and rebuild the whole input layer:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -ForceFetchPrice `
  -ForceBuildAstro `
  -OpenAfter
```

### Custom natal override

If the default natal anchor is not desired, pass natal values directly:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -NatalLabel "nasdaq100_index_1985_ny_open" `
  -NatalLocalDatetime "1985-01-31 09:30:00" `
  -NatalUtcOffsetHours "-5" `
  -NatalLat "40.7128" `
  -NatalLon "-74.0060" `
  -ForceBuildAstro `
  -OpenAfter
```

### Output proof

Every run prints and stores:

```text
RESOLVED_PRICE_CSV=...
RESOLVED_ASTRO_CSV=...
HUMAN_LEARNING_PROTOCOL_DIR=...
```

The manifest also records whether data came from archive, MT5 fetch, or deterministic astro build.


## Antifragile Learning Layer

The Human Learning V2 protocol now includes an antifragile layer by default. This layer does not try to add more and more fragile conditions. It compresses mechanical astro columns into broad concept families, tests simple principles first, compares them with chronological out-of-sample evidence, and stores only stable principles as reusable knowledge.

Main doctrine file:

```text
lab/03_experiments/EXP0016_astro_meta_learner/ANTIFRAGILE_LEARNING_DOCTRINE.md
```

Standalone command:

```powershell
.\tools\astro_ml\build_antifragile_astro_learning_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

Human-learning protocol command with antifragile learning enabled by default:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -OpenAfter
```

Optional neural challenger:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -EnableNeuralChallenger `
  -NeuralMinRows 8000 `
  -OpenAfter
```

The neural model is only a challenger. It is not accepted as knowledge unless it survives the same out-of-sample and gap controls as the simpler models.

Antifragile outputs:

```text
Common\Files\astro_ml\antifragile_memory\<ASSET>\<TIMEFRAME>\<RUN_ID>\
  ANTIFRAGILE_LEARNING_REPORT.md
  antifragile_learning_report.xlsx
  antifragile_mind.json
  antifragile_model_gate.csv
  antifragile_principles.csv
  stable_concepts.csv
  feature_to_concept_map.csv
```
