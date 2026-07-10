  ---
  id: EXP0018-DESIGN-OPERATING-CONTRACT
  title: "EXP0018 Design Operating Contract"
  type: contract
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# قرارداد کار طراحی EXP0018

## اصل مادر

هر مفهوم باید این مسیر را طی کند:

```text
Source claim → Authority classification → Architect decision → Formal rule
→ State/Event/Invariant design → Module/API contract → Test fixture
→ Bounded code patch → Compile/Replay/Visual evidence
```

## قواعد اجباری

- طراحی از کد جلوتر حرکت می‌کند؛ کد حق پرکردن ابهام را ندارد.
- هر Phase یک owner، input/output، state، event، invariant، failure behavior و Definition of Done دارد.
- Core و Optional dependency معکوس ندارند؛ Core نباید برای کارکرد به enrichment نیاز داشته باشد.
- Renderer، CSV و UI فقط projection هستند و منطق تشخیص را تعریف نمی‌کنند.
- هر state mutable دقیقاً یک owner دارد.
- هر تصمیم باز در `EXP0018_OPEN_DECISION_REGISTER` ثبت و به فازهای مسدود متصل است.
- هر patch کوچک، reversible و دارای exact file list است.

## Non-goals

- ورود و خروج معامله
- مدیریت ریسک
- فیلتر خودکار با PDFهای تکمیلی
- ادغام با EXP0017
- مدل آماری یا AI با اختیار تغییر دکترین
