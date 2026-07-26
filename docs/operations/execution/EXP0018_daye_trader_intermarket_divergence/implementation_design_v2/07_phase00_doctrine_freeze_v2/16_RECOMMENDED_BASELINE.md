---
id: EXP0018-P00-RECOMMENDED
title: "EXP0018 Phase 00 — Recommended Baseline"
type: report
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# خط مبنای پیشنهادی برای تصمیم سریع

این سند تصمیم نهایی نیست؛ پیشنهاد مهندسی برای کمترین ابهام و بیشترین قابلیت تست است.

| Decision | پیشنهاد | دلیل |
|---|---|---|
| DY-A01 | High-side=SELL, Low-side=BUY | با مثال صریح LN و منطق weakness/strength سازگارتر است؛ متن Word تعارض دارد و تأیید لازم است. |
| DY-A02 | Tuesday open = Monday 18:00 NY | QT Education صریحاً این mapping را نشان می‌دهد و با futures session labeling سازگار است. |
| DY-A03 | Sunday 18:00 تا Friday 16:59:59 | boundary زمانی پایدار و مستقل از broker candle؛ نیازمند تأیید معمار. |
| DY-A04 | relationship+reference+side+hunter/protected | duplicate را می‌بندد بدون اینکه relationshipهای مستقل را نابود کند. |
| DY-A05 | Current P vs immediately preceding N | با نام‌گذاری زنجیره PA→AL→LN→NP سازگار است. |
| DY-A06 | Wick-touch only in Core | canonical Word همین است؛ body/close نوع event جداست. |
| DY-A07 | 22 Core relationships separate | از مخلوط‌شدن registry با SSMT research جلوگیری می‌کند. |
| DY-A08 | Separate optional module | Core کوچک و قابل QA می‌ماند. |
| DY-A09 | Research-only first | DFR هنوز rule اجرایی تصویب‌شده نیست. |
| DY-A10 | Observer only | triad نباید pair truth را رد کند. |
| DY-A11 | Ledger-only context | نبود اینترنت/خبر نباید Core را متوقف کند. |
| DY-A12 | Keep confirmed lines | Word صریح است و event historical نباید repaint شود. |

## نتیجه در صورت تصویب کامل

با تصویب این baseline:

- P01 می‌تواند review نهایی شود؛
- P02 و P03 code-ready می‌شوند؛
- P04/P05/P07/P08/P10 از blocker خارج می‌شوند؛
- P13 معیار QA قطعی پیدا می‌کند.
