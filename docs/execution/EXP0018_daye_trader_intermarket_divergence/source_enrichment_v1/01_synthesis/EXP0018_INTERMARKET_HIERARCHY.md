# سلسله‌مراتب بین‌بازاری

منابع چند سطح correlation معرفی می‌کنند:

- Indices: NQ / ES / YM و گاهی NKD
- FX: EURUSD / GBPUSD / DXY
- Rates: چند سررسید اوراق به‌عنوان triad
- Metals، energies، crypto، stock triads
- intermarket chain: rates → DXY → FX → indices

Word اصلی فقط دو نماد ورودی دارد. triad و intermarket chain نباید جای pair detector را بگیرد. مسیر پیشنهادی آینده:

1. حفظ pair detector deterministic؛
2. افزودن optional third-symbol observer؛
3. ثبت intermarket context در ledger؛
4. مقایسه آماری pair-only با triad-confirmed؛
5. promotion فقط بعد از out-of-sample evidence.
