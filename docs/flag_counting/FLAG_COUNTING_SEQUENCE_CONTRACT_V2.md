# Flag Counting Sequence Contract V2

این سند نسخه‌ی قفل‌شده‌ی منطقی برای «اف‌شماری / Flag Counting» است. هدفش این است که قبل از هر تغییر کد، قرارداد دقیق تشخیص، زنجیره‌سازی، اینولیدیشن، ND/Hook، ادغام نودها، و نمایش روی چارت روشن باشد.

این سند جایگزین ذهنیت قبلیِ «هر پنجره‌ی ۴ نودی = یک F» می‌شود. در این نسخه، Fها باید در قالب **زنجیره‌ی ترتیبی** دیده شوند: `F1 -> F2 -> F3`. هر F یک بدنه‌ی دو لگ دارد، اما تفاوت F1/F2/F3 در رفتار بعد از بدنه و قواعد invalidation/confirmation است.

---

## 0. اصل مرکزی

منطق اف‌شماری فقط با هندسه‌ی `High / Low` کار می‌کند.

یعنی:

- `open` مهم نیست.
- `close` مهم نیست.
- `body` کندل مهم نیست.
- رنگ کندل مهم نیست.
- wick/body distinction مهم نیست.
- close بالای سطح یا پایین سطح، مفهوم مستقل در این منطق ندارد.

تعبیر دقیق:

```text
The engine is high-low-node based and open/close agnostic.
```

این به معنی «close ممنوع است» نیست؛ یعنی close اصلاً وارد تعریف نمی‌شود. اگر یک حرکت با close هم سطحی را رد کند یا فقط با high/low رد کند، برای این مدل تفاوتی ندارد. معیار فقط nodeهای `High` و `Low` است.

---

## 1. واژگان پایه

### 1.1 Node

هر نقطه‌ی معنی‌دار high یا low در یک scale:

```text
Node = { type: HIGH|LOW, time, price, raw_index, scale_L }
```

### 1.2 Raw Node

همه‌ی high/lowها نگه داشته می‌شوند. هیچ high/low خامی از حافظه‌ی مدل حذف نمی‌شود.

### 1.3 Projected / Compressed Node

در هر context، مدل می‌تواند با scale بزرگ‌تر به نودها نگاه کند. یعنی همه‌ی raw high/lowها در حافظه هستند، اما برای شمارش یک ساختار، آن‌ها را با `L` بزرگ‌تر فشرده می‌کنیم تا sequence خوانا شود.

اصل مهم:

```text
Raw nodes are preserved.
Counting view is scale-compressed.
```

### 1.4 Flag

فلگ یعنی مجموعه‌ی دو لگ:

```text
Flag Body = Leg1 + Leg2
```

هر F، چه F1 چه F2 چه F3، از نظر بدنه‌ی اصلی یک فلگ دو لگه است.

### 1.5 Bullish Flag Body

در حالت صعودی:

```text
Origin Low -> Leg1 High -> Waist Low -> Leg2 High
```

قانون هندسی بدنه:

- Origin باید low باشد.
- Leg1 باید high باشد.
- Waist باید low اصلاحی بعد از Leg1 باشد.
- Leg2 باید high بعد از Waist باشد.
- اصلاح بعد از Leg1 نباید origin / ابتدای لگ را بزند.

### 1.6 Bearish Flag Body

در حالت نزولی:

```text
Origin High -> Leg1 Low -> Waist High -> Leg2 Low
```

قانون هندسی بدنه:

- Origin باید high باشد.
- Leg1 باید low باشد.
- Waist باید high اصلاحی بعد از Leg1 باشد.
- Leg2 باید low بعد از Waist باشد.
- اصلاح بعد از Leg1 نباید origin / ابتدای لگ را بزند.

---

## 2. اصل نگهداری همه‌ی High/Lowها و ادغام context-aware

مدل نباید high/lowهای خام را پاک کند. اما هنگام شمارش، اگر تعداد نودهای یک بخش زیاد شد، باید با scale بزرگ‌تر نگاه کند.

### 2.1 قاعده‌ی عمومی فشرده‌سازی

در همه‌جا:

```text
اگر تعداد نودهای قابل شمارش بیشتر از 4 شد:
    L را بزرگ‌تر کن
    دوباره همان بازه را project کن
    تا جایی ادامه بده که تعداد nodeهای خوانا <= 4 شود
```

### 2.2 چرا این مهم است؟

چون در منطق ما هیچ‌جا ساختار بیشتر از چهار نود برای یک واحد شمارشی نداریم. اگر در raw data بیشتر از چهار نود دیده می‌شود، یعنی باید با scale بزرگ‌تر نگاه کنیم، نه اینکه همه را به‌عنوان ساختار جدا جدا بشماریم.

### 2.3 Raw Preservation Invariant

```text
Invariant:
هیچ raw high/low از حافظه حذف نمی‌شود.
فقط view شمارشی آن‌ها در scaleهای مختلف تغییر می‌کند.
```

---

## 3. شروع زنجیره

### 3.1 Fها پشت سر هم هستند

در یک زنجیره‌ی هم‌اسکیل:

```text
F1 -> F2 -> F3
```

بعد از F1، ساختار بعدی F2 است، نه F1 جدید.
بعد از F2، ساختار بعدی F3 است، نه F1 جدید.

### 3.2 Same-scale Chain

هر زنجیره در یک context/scale دیده می‌شود. ساختارهای داخل همان scale باید زنجیره‌ای باشند:

```text
same chain, same scale-context, ordered F-levels
```

### 3.3 شروع F1

F1 فقط از این دو جا می‌تواند شروع شود:

1. بعد از ND / Hook
2. از انتهای F مخالف

پس F1 نباید از وسط یک موج بی‌هویت شروع شود.

### 3.4 Origin F1

در صعودی:

```text
F1 Origin = یک Low واقعی بعد از ND یا انتهای F مخالف
```

در نزولی:

```text
F1 Origin = یک High واقعی بعد از ND یا انتهای F مخالف
```

اگر origin زده شود، آن origin دیگر اعتبار ندارد و candidate مربوط به آن حذف می‌شود. بعداً با همان origin نباید همان F دوباره زنده شود.

---

## 4. تعریف Leg1

### 4.1 Bullish Leg1

در صعودی، انتهای Leg1 باید بالاترین high قبل از شروع اصلاح باشد.

نه اولین high کوچک.
نه یک high میانی.
نه high خامی که هنوز موج را کامل نکرده.

```text
Bullish Leg1 = highest high before the valid correction begins
```

### 4.2 Bearish Leg1

در نزولی، انتهای Leg1 باید پایین‌ترین low قبل از شروع اصلاح باشد.

```text
Bearish Leg1 = lowest low before the valid correction begins
```

### 4.3 Extension قبل از اصلاح

اگر در جهت لگ چند high/low هم‌جهت بیاید، Leg1 باید تا extreme واقعی آپدیت شود.

مثال صعودی:

```text
Low -> High1 -> High2 -> High3 -> Low correction
Leg1 = High3
```

مثال نزولی:

```text
High -> Low1 -> Low2 -> Low3 -> High correction
Leg1 = Low3
```

---

## 5. Waist / Correction Extreme

### 5.1 تعریف Waist

Waist یعنی extreme واقعی اصلاح بعد از Leg1 و قبل از Leg2.

در صعودی:

```text
Waist = پایین‌ترین Low اصلاح بعد از Leg1 تا قبل از break/extend شدن Leg1
```

در نزولی:

```text
Waist = بالاترین High اصلاح بعد از Leg1 تا قبل از break/extend شدن Leg1
```

### 5.2 Waist باید مدام آپدیت شود

در صعودی:

```text
Leg1 high
correction low 1
correction low 2 deeper
correction low 3 deepest
then break Leg1
Waist = low 3
```

در نزولی:

```text
Leg1 low
correction high 1
correction high 2 higher
correction high 3 highest
then break Leg1 downward
Waist = high 3
```

### 5.3 اگر اصلاح origin را بزند

در صعودی:

```text
Origin Low -> Leg1 High -> correction breaks Origin Low
```

نتیجه:

```text
candidate deleted
origin loses value
view must move to bigger scale if needed
```

در نزولی برعکس.

---

## 6. Leg2 و extension

### 6.1 Leg2

Leg2 حرکت بعد از Waist است که دوباره در جهت فلگ حرکت می‌کند.

در صعودی:

```text
Leg2 = high after Waist, preferably breaking/continuing beyond Leg1
```

در نزولی:

```text
Leg2 = low after Waist, preferably breaking/continuing beyond Leg1
```

### 6.2 اگر بعد از تشکیل فلگ، 1/2 نیاید و انتهای فلگ رد شود

این یکی از مهم‌ترین قواعد است.

در F1:

اگر بدنه‌ی فلگ ساخته شد، اما هنوز post-flag internal `1/2` نداده و بازار دوباره انتهای فلگ را رد کرد، آن حرکت جدید هنوز بخشی از همان فلگ اصلی و extension لگ دوم است.

در صعودی:

```text
Origin Low -> Leg1 High -> Waist Low -> Leg2 High
no internal 1/2 yet
price makes new high beyond Leg2
=> new high becomes extended Leg2
=> previous Leg2 high is ignored for final body
```

در نزولی برعکس.

### 6.3 این قاعده برای F2 هم هست

در F2 هم اگر بعد از فلگ هنوز post-flag `1/2` نیامده و حرکت در جهت فلگ ادامه داد، continuation به‌عنوان extension همان Leg2 حساب می‌شود.

### 6.4 F3

F3 بعد از بدنه‌ی دو لگ کامل می‌شود. بعد از F3 دیگر post-flag correction برای اعتبار F3 لازم نیست.

---

## 7. Internal 1/2 بعد از فلگ

### 7.1 محل ساخت internal 1/2

`1` و `2` در اصلاح بعد از Leg2 ساخته می‌شوند؛ یعنی بعد از اینکه فلگ دو لگه ساخته شد.

### 7.2 Bullish internal 1/2

بعد از یک bullish flag:

```text
Leg2 High
internal 1 = Low after Leg2
middle node = High between 1 and 2
internal 2 = Lower Low after middle node
```

شرط:

```text
internal 2 باید زیر internal 1 باشد
```

یعنی در صعودی:

```text
2 < 1
```

ساختار:

```text
Low(1) -> High(middle) -> Lower Low(2)
```

### 7.3 Bearish internal 1/2

بعد از یک bearish flag:

```text
Leg2 Low
internal 1 = High after Leg2
middle node = Low between 1 and 2
internal 2 = Higher High after middle node
```

شرط:

```text
internal 2 باید بالای internal 1 باشد
```

یعنی در نزولی:

```text
2 > 1
```

ساختار:

```text
High(1) -> Low(middle) -> Higher High(2)
```

### 7.4 شرط خاص F1

در F1، middle node بین `1` و `2` نباید انتهای فلگ F1 را بشکند.

در bullish F1:

```text
middle high نباید بالاتر از Leg2 high / flag end باشد
```

در bearish F1:

```text
middle low نباید پایین‌تر از Leg2 low / flag end باشد
```

اگر middle node این حد را بشکند، آن 1/2 برای F1 معتبر نیست؛ بلکه باید به‌عنوان extension یا context بزرگ‌تر بررسی شود.

### 7.5 شرط F2

در F2، middle node بین `1` و `2` می‌تواند انتهای فلگ / Leg2 را رد کند.

در bullish F2:

```text
middle high می‌تواند بالاتر از Leg2 high برود
```

در bearish F2:

```text
middle low می‌تواند پایین‌تر از Leg2 low برود
```

### 7.6 F3 post-flag 1/2 ندارد

برای F3، اصلاح بعد از فلگ برای اعتبار خودش اهمیتی ندارد.

---

## 8. F1 Contract

### 8.1 بدنه‌ی F1

F1 یک فلگ دو لگه است:

Bullish:

```text
Origin Low -> Leg1 High -> Waist Low -> Leg2 High
```

Bearish:

```text
Origin High -> Leg1 Low -> Waist High -> Leg2 Low
```

### 8.2 Invalidation F1

در F1، کمر فلگ / Waist نقش invalidation بعد از تشکیل فلگ را دارد.

Bullish F1:

```text
اگر بعد از تشکیل بدنه و قبل از confirmation، قیمت Waist Low را بزند، F1 invalid می‌شود.
```

Bearish F1:

```text
اگر بعد از تشکیل بدنه و قبل از confirmation، قیمت Waist High را بزند، F1 invalid می‌شود.
```

### 8.3 قبل از کامل شدن فلگ

اگر اصلاح بعد از Leg1، ابتدای Leg1 / Origin را بزند، candidate حذف می‌شود و باید با دید بزرگ‌تر بررسی شود.

### 8.4 F1 Candidate

F1 candidate باید دیده شود، حتی اگر هنوز confirmed نشده است.

نمایش باید status داشته باشد:

```text
F1 candidate / live
F1 confirmed
F1 invalidated only in audit, not main chart
```

### 8.5 F1 Confirmation

F1 وقتی تأیید می‌شود که:

1. بدنه‌ی دو لگه داشته باشد.
2. بعد از Leg2، حداقل `1/2` معتبر بدهد.
3. این `1/2` قبل از زدن Waist رخ دهد.
4. بعد از `1/2`، دوباره انتهای فلگ را با high/low بزند یا بشکند.

Bullish confirmation:

```text
F1 body completed
post-flag 1/2 completed before Waist hit
then High breaks/reaches Leg2 high / extended flag end
=> F1 confirmed
```

Bearish confirmation:

```text
F1 body completed
post-flag 1/2 completed before Waist hit
then Low breaks/reaches Leg2 low / extended flag end
=> F1 confirmed
```

### 8.6 اگر 1/2 نیاید و انتهای فلگ رد شود

تا وقتی `1/2` نیامده، هر continuation در جهت فلگ، extension لگ دوم است.

```text
No 1/2 yet => no confirmation yet => continuation extends Leg2
```

### 8.7 اگر بیشتر از 2 نود بعد از فلگ آمد

اگر بعد از فلگ، نودهای اصلاحی بیشتر شد، باید با منطق compression آن‌ها را تا حداکثر 4 نود ببینیم.

اگر بعد از compression تعداد نودها 3 یا 4 شد، آنجا ND/Hook هم label می‌گیرد.

دو نود به‌تنهایی ND نیست.

---

## 9. F2 Contract

### 9.1 F2 فقط بعد از confirmation F1 ساخته می‌شود

F2 نباید روی F1 خام ساخته شود.

```text
F2 spawn allowed only after F1 confirmed
```

### 9.2 F2 Origin

F2 از انتهای اصلاح بعد از فلگ F1 شروع می‌شود؛ یعنی از جایی که بعد از دو لگ F1، post-flag correction داده و `1/2` یا بیشتر ساخته شده است.

در عمل:

```text
F2 Origin = effective end of F1 post-flag correction
```

اگر post-flag correction فقط `1/2` ساده باشد، این همان internal 2 است.
اگر بیشتر از 2 نود باشد، بعد از compression، effective correction end همان نقطه‌ای است که زنجیره آن را به‌عنوان مبدا F2 می‌پذیرد.

### 9.3 F2 Body

F2 هم یک فلگ دو لگه است.

Bullish F2:

```text
F2 Origin Low -> Leg1 High -> Waist Low -> Leg2 High
```

Bearish F2:

```text
F2 Origin High -> Leg1 Low -> Waist High -> Leg2 Low
```

### 9.4 F2 Invalidation

در F2، invalidation اصلی ابتدای لگ اول / Origin است، نه Waist.

Bullish F2:

```text
اگر F2 Origin Low زده شود، F2 invalid می‌شود.
```

Bearish F2:

```text
اگر F2 Origin High زده شود، F2 invalid می‌شود.
```

### 9.5 اگر F2 Origin زده شد

اگر F2 ابتدای خودش را زد:

- F2 دیگر معتبر نیست.
- اما هنوز داخل context F1 حساب می‌شود.
- F1 parent اگر invalid نشده، زنده است.
- موتور همچنان دنبال F2 جدید برای همان F1 می‌گردد.

```text
F2 origin hit => remove F2 candidate, keep F1 alive, continue searching F2 while F1 alive
```

### 9.6 F2 Waist Break Branch

در F2، اگر Waist شکسته شود ولی Origin شکسته نشود، این invalid نیست. این می‌تواند branch مخصوص F2 باشد.

در این حالت:

```text
1 = F2 Waist
2 = node that breaks F2 Waist
```

یعنی F2 اجازه دارد کمر فلگ خودش را بزند، به شرط اینکه ابتدای لگ خودش را نزند.

### 9.7 F2 Confirmation

F2 وقتی تأیید می‌شود که:

1. بدنه‌ی فلگ داشته باشد.
2. `1/2` یا بیشتر بعد از فلگ بسازد.
3. می‌تواند Waist را بزند، ولی Origin را نباید بزند.
4. بعد دوباره انتهای فلگ / Leg2 را با high/low بشکند یا بزند.

### 9.8 شرط اندازه F2 نسبت به F1

اندازه‌ی فلگ:

```text
Flag size = abs(Leg2.price - Origin.price)
```

شرط F2:

```text
F2 flag size >= F1 flag size
```

این شرط بر اساس فاصله‌ی ابتدای لگ اول تا انتهای لگ دوم است.

---

## 10. F3 Contract

### 10.1 F3 فقط بعد از F2 زنده/معتبر ساخته می‌شود

تا وقتی F2 زنده است، موتور دنبال F3 می‌گردد.

### 10.2 F3 Origin

F3 از انتهای اصلاح بعد از F2 شروع می‌شود؛ یعنی از effective correction end بعد از F2.

### 10.3 F3 Body Enough

برای F3، بدنه‌ی دو لگه کافی است.

```text
F3 = completed flag body
```

F3 نیازی به post-flag `1/2` ندارد.

### 10.4 F3 Same-scale Requirement

F3 باید با F1 و F2 در یک context scale قابل قبول باشد.

این بخش هنوز تصمیم اجرایی دقیق لازم دارد، چون «هم‌اسکیل بودن» باید به یک معیار عددی تبدیل شود.

Open decision:

```text
Same-scale F1/F2/F3 = ?
```

گزینه‌های ممکن برای تعریف مهندسی:

1. همان `scale_L` دقیق.
2. scale_L در یک band قابل قبول، مثلاً ±1 step.
3. similarity بر اساس flag size ratio.
4. ترکیب scale_L و flag size.

تا قبل از قفل شدن این تصمیم، پیاده‌سازی باید این قسمت را input-driven نگه دارد.

### 10.5 F3 Lock

وقتی F3 تکمیل شد:

- کل حرکت بعدی در همان جهت می‌تواند extension F3 حساب شود.
- ساختار sequence بسته و قفل می‌شود.
- حتی اگر بازار کل حرکت را برگردد، F3 از چارت حذف نمی‌شود.
- چون F3 «کار خودش را کرده است».

```text
F3 complete => sequence locked
locked sequence never deleted from main historical display
```

### 10.6 پایان sequence بعد از F3

بعد از F3، با تشکیل ریزترین F1 مخالف، extent نهایی F3 تا همانجایی که رسیده قفل می‌شود و sequence پایان می‌یابد.

Open engineering detail:

```text
smallest opposite F1 = which scale? minimum raw scale? selected minor scale? adaptive smallest stable F1?
```

این بخش باید بعداً به input/algorithm دقیق تبدیل شود.

---

## 11. ND / Hook Contract

### 11.1 ND چیست؟

ND / Hook یک فاز یا چرخه‌ی نودی است، نه الزاماً یک فلگ.

ND زمانی مهم است که نودها به شکلی 3 یا 4 نودی در یک cycle قابل خواندن باشند، مخصوصاً وقتی ساختار F در آن context هنوز شکل نگرفته یا نودها بیش از حد ریز و شلوغ شده‌اند.

### 11.2 ND بر اساس High/Low است

ND هم فقط با high/low nodeها تعریف می‌شود.

```text
ND is high-low-node based and close-agnostic.
```

### 11.3 قانون تعداد نود ND

ND بعد از compression باید 3 یا 4 نود داشته باشد.

```text
2 nodes => not ND
3 nodes => ND candidate
4 nodes => ND candidate
>4 nodes => increase L until <=4
```

### 11.4 اگر raw nodes بیشتر از 4 شد

اگر در یک بازه‌ی ND تعداد nodeها بیشتر از 4 شد:

```text
increase L
reproject nodes
repeat until node_count <= 4
```

### 11.5 L مبدا در ND

در ND، L نود مبدا به صورت پایه 2 در نظر گرفته می‌شود و خود مبدا را با افزایش L حذف/جابجا نمی‌کنیم. افزایش L برای readable کردن ادامه‌ی cycle انجام می‌شود.

Open engineering detail:

```text
Origin node L is pinned at 2.
Projection of subsequent nodes adapts upward until the visible ND cycle has <=4 nodes.
```

این باید در کد به شکل واضح جدا از compression عمومی پیاده شود.

### 11.6 شرط 50 درصد cycle

ND پیش‌فرض باید فقط وقتی قبول شود که cycle حداقل 50% بازه‌ی خودش را طی کرده باشد.

تعریف بازه:

```text
cycle_start = first ND node price
cycle_extreme = furthest price reached inside ND cycle
range = abs(cycle_extreme - cycle_start)
```

شرط پیش‌فرض:

```text
movement >= 0.50 * range_basis
```

چون close نداریم، این شرط هم فقط با high/low nodeها سنجیده می‌شود.

### 11.7 زیر 50 درصد

باید input داشته باشیم که زیر 50% را هم قبول کند.

پیشنهاد input:

```text
InpNDRequireMinCycleRatio = true
InpNDMinCycleRatio = 0.50
```

اگر خاموش شود:

```text
3/4-node ND structure is accepted even below 50%
```

### 11.8 ND داخل F هم نمایش داده می‌شود

اگر ND و F overlap داشته باشند، هر دو نمایش داده می‌شوند.

```text
F body can exist
ND label can also exist
```

ND برای جلوگیری از شلوغی فقط text-only است، مگر اینکه debug mode بخواهد shape هم بکشد.

### 11.9 ND در F1/F2 extension context

وقتی بعد از فلگ، تعداد اصلاحی/چرخه‌ای بیشتر از 2 شد و بعد از compression به 3 یا 4 رسید، آن ناحیه ND هم حساب می‌شود و باید label بگیرد.

---

## 12. Sequence Engine

### 12.1 زنجیره‌ی اصلی

هر sequence این lifecycle را دارد:

```text
WAIT_F1
F1_LIVE
F1_CONFIRMED
SEARCH_F2
F2_LIVE
F2_CONFIRMED
SEARCH_F3
F3_LIVE
F3_LOCKED
DONE
```

### 12.2 F-level reset ممنوع در همان chain

در یک chain:

```text
After F1 => next F is F2
After F2 => next F is F3
After F3 => chain locks/done
```

پس نباید بعد از F1 دوباره F1 جدید در همان chain ساخته شود.

### 12.3 F1 جدید کجا مجاز است؟

F1 جدید فقط برای chain جدید مجاز است:

- بعد از ND مستقل
- بعد از انتهای F مخالف
- بعد از پایان sequence قبلی و شروع context مخالف/جدید

### 12.4 Parent/Child

F1 parent برای F2 است.
F2 parent برای F3 است.

اگر child invalid شود، parent زنده می‌ماند مگر invalidation خودش خورده باشد.

```text
child invalidation does not kill parent
```

### 12.5 ادامه‌ی جست‌وجو بعد از child invalidation

اگر F2 invalid شد ولی F1 هنوز زنده/confirmed است، موتور همان F1 را ادامه می‌دهد و همچنان دنبال F2 می‌گردد.

اگر F3 invalid/candidate-fail شد ولی F2 هنوز زنده/confirmed است، موتور همان F2 را ادامه می‌دهد و همچنان دنبال F3 می‌گردد.

---

## 13. Candidate / Confirmed / Locked / Rejected

### 13.1 Candidate

ساختاری که هنوز confirmation کامل ندارد، اما برای research view باید دیده شود.

### 13.2 Confirmed

ساختاری که قرارداد تایید خودش را پاس کرده.

### 13.3 Locked

فقط sequenceهایی که F3 complete کرده‌اند locked می‌شوند. Lockedها نباید از historical display پاک شوند.

### 13.4 Rejected / Invalidated

Rejectedها روی چارت اصلی نمایش داده نمی‌شوند.

آن‌ها فقط در audit/log/report می‌آیند.

```text
Main chart = live + confirmed + locked + ND
Audit = includes rejected/invalidated
```

---

## 14. Duplicate Rules

اگر دو sequence همه‌ی مشخصات هندسی و هویتی‌شان دقیقاً یکسان باشد، نباید دو بار نمایش داده شوند.

مشخصات identity:

```text
symbol
timeframe
scale_context
sequence direction
F level
origin node
leg1 node
waist node
leg2 node
internal nodes if applicable
parent id if applicable
status
```

اگر همه چیز عین هم بود:

```text
merge into one display object
```

اگر حتی یک تفاوت کوچک وجود داشت:

```text
keep as separate sequence
```

---

## 15. Rendering Contract

### 15.1 همه دیده شوند

نمایش پیش‌فرض باید همه‌ی موارد زنده/confirmed/locked/ND را نشان دهد.

نه فقط dominant.
نه فقط selected scale.

### 15.2 Rejectedها دیده نشوند

Rejected/invalidated روی چارت اصلی نمانند.

### 15.3 line width

همه‌ی خطوط نازک و هم‌سایز باشند.

```text
Fixed line width = 1 by default
```

scale بزرگ‌تر نباید خط ضخیم‌تر بگیرد، چون چارت را شلوغ می‌کند.

### 15.4 Sequence shade

برای اینکه sequenceها از هم قابل تفکیک باشند، هر sequence باید shade کمی متفاوت از همان خانواده رنگ بگیرد.

مثلاً:

```text
Bullish candidate = blue/cyan family, shades by sequence id
Bullish confirmed = green family, shades by sequence id
Bearish candidate = orange/red family, shades by sequence id
Bearish confirmed = red family, shades by sequence id
ND = neutral/silver family
F3 locked = distinct but still thin
```

### 15.5 Label detail

فعلاً label باید گزینه C باشد:

```text
F1 L8 Q23
F2 L8 Q23
F3 L8 Q23
ND L8 Q23
```

یعنی:

- F level
- scale L
- sequence id / chain id

### 15.6 Origin label

فعلاً origin با `O` کوچک نشان داده شود.

Input پیشنهادی:

```text
InpShowOriginLabels = true
```

### 15.7 Label placement

قله‌ها:

```text
labels above peak
```

دره‌ها:

```text
labels below valley
```

### 15.8 Stack order

اگر چند label در یک ناحیه جمع شدند، نزدیک‌ترین label به قیمت باید قدیمی‌ترین باشد.

ترتیب از نزدیک به دور:

1. older sequence first
2. larger scale if same age/context
3. higher F level if still tied
4. confirmed before candidate if still tied
5. ND after F labels unless same identity requires otherwise

### 15.9 Curve contract

بدنه‌ی F باید این‌طور رسم شود:

```text
Origin -> Leg1 = straight line
Leg1 -> Leg2 = smooth curve through Waist
```

Curve فقط باید از waist / انتهای اصلاح عبور کند. لازم نیست مسیر کندل‌ها را مو به مو دنبال کند.

مهم این است که:

- شکسته و چند trendline خشن نباشد.
- از Waist واقعی رد شود.
- visually مشخص کند این یک بدنه‌ی دو لگه است.

### 15.10 ND Rendering

ND فعلاً text-only است.

```text
ND L8 Q23
```

اگر با F overlap دارد، هر دو نمایش داده می‌شوند، اما ND خط اضافه نمی‌کشد.

---

## 16. Algorithmic Modules

### 16.1 Node Engine

مسئولیت‌ها:

- استخراج raw high/low nodes
- نگهداری همه‌ی raw nodes
- ساخت projection بر اساس scale L
- فشرده‌سازی alternating view
- حفظ identity mapping از projected node به raw nodes

نباید:

- close/open را وارد کند.
- raw nodes را حذف کند.
- با window خام هر 4 node را F فرض کند.

### 16.2 Scale Compression Engine

مسئولیت‌ها:

- گرفتن یک بازه‌ی nodeها
- افزایش L تا وقتی node_count <= 4 شود
- برای ND، pin کردن origin L=2 طبق قرارداد
- خروجی دادن projected readable sequence

### 16.3 Flag Body Detector

مسئولیت‌ها:

- پیدا کردن Origin, Leg1, Waist, Leg2
- آپدیت Leg1 تا extreme واقعی قبل از correction
- آپدیت Waist تا deepest/highest correction extreme
- extension دادن Leg2 اگر post-flag 1/2 هنوز نیامده
- رعایت invalidation پیش از تکمیل body

### 16.4 Post-Flag Internal Detector

مسئولیت‌ها:

- تشخیص internal 1/2 بعد از Leg2
- رعایت قاعده‌ی F1 middle-node not breaking flag end
- اجازه دادن به F2 middle-node برای عبور از flag end
- compression کردن نودهای بیشتر از 4
- تولید ND label اگر 3/4 node cycle شکل گرفت

### 16.5 Sequence Engine

مسئولیت‌ها:

- مدیریت lifecycle F1->F2->F3
- جلوگیری از reset اشتباه F-level در همان chain
- نگه داشتن parent هنگام invalid شدن child
- شروع F2 فقط بعد از confirmation F1
- جست‌وجوی F2 تا وقتی F1 زنده است
- جست‌وجوی F3 تا وقتی F2 زنده است
- قفل کردن sequence بعد از F3

### 16.6 ND / Hook Detector

مسئولیت‌ها:

- اسکن 3/4-node cycles بعد از compression
- اعمال 50% cycle threshold در حالت پیش‌فرض
- اجازه‌ی input برای قبول زیر 50%
- نمایش ND حتی داخل Fها
- text-only rendering by default

### 16.7 Identity / Dedup Engine

مسئولیت‌ها:

- ساخت key برای هر event/sequence
- merge کردن فقط وقتی همه‌ی مشخصات دقیقاً یکی است
- جدا نگه داشتن حتی با تفاوت کوچک

### 16.8 Renderer

مسئولیت‌ها:

- نمایش همه‌ی live/confirmed/locked/ND
- عدم نمایش rejectedها
- خطوط نازک ثابت
- shade متفاوت برای sequenceها
- label کامل F/L/Q
- O label برای origin
- stack مرتب و deterministic
- curve نرم از Leg1 به Leg2 از طریق Waist

---

## 17. Pseudocode سطح بالا

### 17.1 Main scan

```pseudo
raw_nodes = NodeEngine.extract_high_low_nodes(rates)
all_scales = ScaleEngine.build_views(raw_nodes)

for each scale_view:
    detect_nd_hooks(scale_view)
    update_or_start_sequences(scale_view)
```

### 17.2 Sequence update

```pseudo
for each sequence in active_sequences:
    if sequence.state == WAIT_F1:
        try_start_f1_after_nd_or_opposite_f_end()

    if sequence.state == F1_LIVE:
        update_f1_body_and_post_flag()
        if f1_waist_hit_after_body_before_confirmation:
            invalidate_f1()
        if f1_confirmed:
            sequence.state = SEARCH_F2

    if sequence.state == SEARCH_F2:
        try_start_f2_from_f1_effective_post_flag_correction_end()

    if sequence.state == F2_LIVE:
        update_f2_body_and_post_flag()
        if f2_origin_hit:
            remove_f2_keep_f1_searching()
        if f2_confirmed:
            sequence.state = SEARCH_F3

    if sequence.state == SEARCH_F3:
        try_start_f3_from_f2_effective_post_flag_correction_end()

    if sequence.state == F3_LIVE:
        if f3_body_completed:
            lock_f3_sequence()
```

### 17.3 Body detection

```pseudo
function detect_flag_body(origin, direction):
    leg1 = find_directional_extreme_before_first_valid_correction(origin, direction)
    waist = find_deepest_opposite_correction_extreme(leg1, direction)

    if correction_hits_origin_before_leg2:
        return invalid_candidate

    leg2 = find_directional_move_after_waist(direction)

    while no_internal_12_after_leg2 and price_extends_beyond_leg2:
        leg2 = extended_extreme

    return body(origin, leg1, waist, leg2)
```

### 17.4 Internal 1/2 bullish

```pseudo
function detect_bullish_internal_12_after_leg2(leg2):
    one = first_low_after_leg2
    middle = high_after_one
    two = lower_low_after_middle

    require two.price < one.price

    if current_f_level == F1:
        require middle.price <= leg2.price

    return one, middle, two
```

### 17.5 Internal 1/2 bearish

```pseudo
function detect_bearish_internal_12_after_leg2(leg2):
    one = first_high_after_leg2
    middle = low_after_one
    two = higher_high_after_middle

    require two.price > one.price

    if current_f_level == F1:
        require middle.price >= leg2.price

    return one, middle, two
```

### 17.6 F1 confirmation

```pseudo
if f_level == F1:
    body_completed
    internal_12_completed_before_waist_hit
    flag_end_rehit_or_break_by_high_low
    => confirmed
```

### 17.7 F2 confirmation

```pseudo
if f_level == F2:
    body_completed
    internal_12_completed_or_more
    origin_not_hit
    flag_end_rehit_or_break_by_high_low
    => confirmed
```

### 17.8 F3 lock

```pseudo
if f_level == F3 and body_completed:
    state = F3_LOCKED
    keep_extending_f3_until_smallest_opposite_f1
    never delete locked sequence
```

---

## 18. خطاهایی که کد نباید تکرار کند

### 18.1 هر 4 نود یک F نیست

غلط:

```text
L-H-L-H window => F
```

درست:

```text
F باید در sequence context باشد و origin/leg1/waist/leg2 معتبر داشته باشد.
```

### 18.2 شروع از وسط موج غلط است

هر خطی که origin واقعی ندارد نباید روی چارت بیاید.

### 18.3 اگر ابتدای لگ خورد، candidate مرده است

برای candidate همان F:

```text
origin hit => candidate deleted
```

اما parent زنده می‌ماند اگر invalidation خودش نخورده باشد.

### 18.4 F2 بعد از F1 دوباره F1 نیست

غلط:

```text
F1 confirmed -> new F1
```

درست:

```text
F1 confirmed -> search F2
```

### 18.5 F3 نباید پاک شود

وقتی F3 قفل شد، با برگشت بعدی حذف نمی‌شود.

### 18.6 Waist اشتباه ممنوع

در صعودی، waist باید lowest low correction باشد.
در نزولی، waist باید highest high correction باشد.

### 18.7 خطوط شکسته‌ی curve ممنوع

curve نباید با چند trendline شکسته‌ی خشن نمایش داده شود. باید smooth باشد و از Waist رد شود.

---

## 19. Inputs پیشنهادی

```text
InpShowAllLiveSequences = true
InpShowRejectedOnMainChart = false
InpShowOriginLabels = true
InpDetailedLabels = true
InpFixedLineWidth = 1
InpUseSequenceColorShades = true

InpNDRequireMinCycleRatio = true
InpNDMinCycleRatio = 0.50
InpNDAcceptBelowMinRatio = false
InpDrawNDText = true
InpDrawNDLines = false

InpRequireF1ConfirmedBeforeF2 = true
InpRequireF2ConfirmedBeforeF3 = true
InpLockF3AfterBody = true
InpKeepLockedF3OnChart = true

InpSameScaleMode = SCALE_L_EXACT_OR_OPEN_DECISION
InpSameScaleTolerance = 0
```

---

## 20. Open decisions باقی‌مانده

این‌ها هنوز باید قبل از نسخه‌ی نهایی کد قفل شوند:

### OD1. تعریف عددی هم‌اسکیل بودن F1/F2/F3

کاربر گفت F3 باید هم‌اسکیل F1 و F2 باشد، اما معیار عددی باید تعیین شود.

گزینه‌های قابل بررسی:

```text
A) same exact scale_L
B) scale_L within tolerance
C) flag size ratio band
D) hybrid scale_L + flag size ratio
```

### OD2. کوچک‌ترین F1 مخالف بعد از F3

بعد از F3، حرکت همان جهت ادامه‌ی F3 حساب می‌شود تا ریزترین F1 مخالف ظاهر شود. باید تعریف شود «ریزترین» یعنی چه.

گزینه‌ها:

```text
A) minimum available L
B) smallest stable confirmed opposite F1
C) smallest candidate opposite F1
D) user-selected minor scale
```

### OD3. ND pinned origin L=2 implementation

اصل قطعی است، ولی شکل اجرایی دقیق باید در کد مشخص شود:

```text
origin L pinned at 2, subsequent nodes compressed adaptively
```

### OD4. F2 effective correction end when more than 2 post-F1 nodes exist

اگر بعد از F1 بیش از 2 نود post-flag correction باشد، F2 از effective correction end شروع می‌شود. باید فرمول دقیق انتخاب این end در حالت 3/4-node ND نهایی شود.

پیشنهاد اولیه:

```text
Bullish chain: F2 origin = last effective low/correction node after F1 post-flag compression
Bearish chain: F2 origin = last effective high/correction node after F1 post-flag compression
```

---

## 21. Acceptance Criteria برای پیاده‌سازی بعدی

کد درست است اگر:

1. هیچ F از وسط موج بی‌هویت شروع نشود.
2. هر خط روی چارت label داشته باشد که بگوید F چند، scale چند، sequence چند.
3. Origin هر F با O قابل دیدن باشد.
4. F بعد از F1 در همان chain حتماً F2 باشد، نه F1 جدید.
5. F بعد از F2 حتماً F3 باشد، نه F1 جدید.
6. F1 بدون confirmation می‌تواند candidate باشد و دیده شود.
7. F2 فقط بعد از F1 confirmed ساخته شود.
8. F3 فقط بعد از F2 ساخته شود.
9. F3 بعد از تکمیل body قفل شود و پاک نشود.
10. NDهای 3/4-node دیده شوند.
11. NDهای زیر 50% فقط اگر input اجازه دهد قبول شوند.
12. هیچ منطق open/close در detector نباشد.
13. Waist در bullish lowest correction low باشد.
14. Waist در bearish highest correction high باشد.
15. خطوط نازک باشند.
16. Labels stack شوند و rejectedها روی چارت اصلی دیده نشوند.

---

## 22. خلاصه نهایی

اف‌شماری یک pattern scanner خام نیست. یک sequence engine است.

موتور باید:

- همه‌ی high/lowها را نگه دارد.
- با scale بزرگ‌تر آن‌ها را فشرده کند.
- از ND یا انتهای F مخالف، F1 بسازد.
- بعد از F1 confirmed دنبال F2 بگردد.
- بعد از F2 دنبال F3 بگردد.
- F3 را بعد از body قفل کند.
- candidateها را نمایش دهد، rejectedها را نه.
- هیچ چیز را با close/open تعریف نکند.
- هر رسم را به identity واقعی خودش وصل کند.

