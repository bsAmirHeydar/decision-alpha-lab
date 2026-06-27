# Flag Counting V2 Implementation Checklist

این چک‌لیست برای تبدیل `FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md` به کد است. هر آیتم باید یا در کد پیاده شود یا عمداً با TODO مشخص بماند.

## A. Node Engine

- [ ] تمام high/low raw nodes نگه داشته شوند.
- [ ] open/close/body/color وارد node logic نشوند.
- [ ] projected nodes به raw nodes map داشته باشند.
- [ ] same-type consecutive nodes در projection به extreme معتبر فشرده شوند.
- [ ] compression context-aware باشد و raw data را حذف نکند.

## B. Scale / Compression

- [ ] اگر شمارش یک بخش >4 node شد، L افزایش یابد تا <=4 شود.
- [ ] ND origin L=2 pinned شود.
- [ ] برای ND، subsequent nodes با L بزرگ‌تر readable شوند.
- [ ] هر projection باید identity مستقل داشته باشد.

## C. Flag Body

- [ ] Bullish origin = low.
- [ ] Bearish origin = high.
- [ ] Bullish Leg1 = highest high before correction.
- [ ] Bearish Leg1 = lowest low before correction.
- [ ] Bullish Waist = lowest correction low.
- [ ] Bearish Waist = highest correction high.
- [ ] Leg2 تا قبل از internal 1/2 extension بخورد.
- [ ] اگر correction origin را زد، candidate حذف شود.

## D. Internal 1/2

- [ ] Bullish post-flag: low(1), high(middle), lower low(2).
- [ ] Bearish post-flag: high(1), low(middle), higher high(2).
- [ ] F1 middle node نباید flag end را بشکند.
- [ ] F2 middle node می‌تواند flag end را بشکند.
- [ ] F3 post-flag internal نیاز ندارد.

## E. F1

- [ ] F1 فقط بعد از ND یا انتهای F مخالف شروع شود.
- [ ] F1 candidate نمایش داده شود.
- [ ] F1 invalidation after body = waist.
- [ ] F1 confirmation = valid 1/2 before waist hit + rehit/break of flag end.

## F. F2

- [ ] F2 فقط بعد از F1 confirmed ساخته شود.
- [ ] F2 origin = effective end of F1 post-flag correction.
- [ ] F2 invalidation = own origin/start of leg1.
- [ ] F2 can break its waist branch if origin survives.
- [ ] F2 size >= F1 size.
- [ ] اگر F2 invalid شد، F1 parent زنده بماند و search F2 ادامه یابد.

## G. F3

- [ ] F3 فقط بعد از F2 ساخته شود.
- [ ] F3 body complete کافی است.
- [ ] F3 same-scale with F1/F2 as open decision input باشد.
- [ ] F3 بعد از body locked شود.
- [ ] Locked F3 از چارت پاک نشود.
- [ ] Same-direction extension بعد از F3 به F3 وصل شود تا opposite smallest F1.

## H. ND / Hook

- [ ] ND فقط high/low based باشد.
- [ ] 2 node ND نیست.
- [ ] 3 یا 4 node ND candidate است.
- [ ] >4 node => increase L until <=4.
- [ ] 50% cycle ratio پیش‌فرض فعال باشد.
- [ ] input برای قبول زیر 50% وجود داشته باشد.
- [ ] ND داخل F هم نمایش داده شود.
- [ ] ND text-only by default باشد.

## I. Sequence Identity

- [ ] در هر chain بعد از F1 فقط F2 ساخته شود.
- [ ] بعد از F2 فقط F3 ساخته شود.
- [ ] child invalidation parent را نکشد.
- [ ] rejectedها main chart را ترک کنند.
- [ ] duplicate فقط وقتی merge شود که تمام مشخصات یکی باشد.

## J. Renderer

- [ ] همه‌ی live/confirmed/locked/ND نمایش داده شوند.
- [ ] rejectedها نمایش داده نشوند.
- [ ] همه‌ی خطوط width=1 باشند.
- [ ] shade هر sequence متفاوت باشد.
- [ ] label = `F1 L8 Q23` style باشد.
- [ ] origin label `O` فعال باشد.
- [ ] قله‌ها label بالای قله؛ دره‌ها label زیر دره.
- [ ] قدیمی‌تر نزدیک‌تر به قیمت stack شود.
- [ ] curve = straight Origin->Leg1 + smooth Leg1->Leg2 through Waist.

## K. Open Decisions to implement as Inputs

- [ ] Same-scale mode for F1/F2/F3.
- [ ] Smallest opposite F1 definition after F3.
- [ ] Effective correction end when post-flag correction has 3/4 nodes.
- [ ] ND pinned-origin-L exact implementation.
