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
