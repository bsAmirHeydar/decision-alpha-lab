# Level 22 — STC SMT Hidden Offline License Fix

## هدف

این اصلاح برای پروژه‌ی STC / SMT Cycles است و عمداً inputهای لایسنس را مخفی/غیرمستقیم نگه می‌دارد.

هیچ input واضحی با اسم license اضافه نمی‌شود.

## ورودی‌های مخفی لایسنس

لایسنس همچنان از همین inputهای ظاهراً Cycle Model خوانده می‌شود:

```text
InpCycleModelProfile      = license token
InpCycleOperatorMemo      = passphrase
InpCycleReferenceSeed     = gate A
InpCycleDivergenceSeed    = gate B
InpCycleExecutionSeed     = gate C
InpCycleReleaseSeed       = gate D
InpCycleCacheDepthMinutes = recheck interval in minutes
```

## چیزی که درست شد

- هیچ input واضحی با اسم مستقیم license اضافه نشده است.
- license engine حالا account-any را هم می‌فهمد.
- server-any از مقدار `ANY` پشتیبانی می‌کند.
- audit حالا دقیق‌تر می‌گوید mismatch از account است یا server یا signature یا gate.
- keygen خروجی recipient را فقط با inputهای مخفی `InpCycle...` چاپ می‌کند.
- bug تکرار دوباره‌ی نوشتن issuer audit در keygen حذف شد.

## account-any

برای لایسنسی که روی هر اکانت کار کند:

```powershell
python tools\stc_smt_deployment\offline_license_keygen.py `
  --account-any `
  --server-any `
  --expires 20261231 `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar
```

خروجی recipient فقط این‌هاست:

```text
InpCycleModelProfile=...
InpCycleOperatorMemo=...
InpCycleReferenceSeed=...
InpCycleDivergenceSeed=...
InpCycleExecutionSeed=...
InpCycleReleaseSeed=...
```

## account-bound

برای لایسنس محدود به اکانت خاص:

```powershell
python tools\stc_smt_deployment\offline_license_keygen.py `
  --account 12345678 `
  --server-any `
  --expires 20261231 `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar
```

## server-bound

برای bind به سرور خاص بروکر:

```powershell
python tools\stc_smt_deployment\offline_license_keygen.py `
  --account 12345678 `
  --server "Broker-Server-Name" `
  --expires 20261231 `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar
```

## نکته‌ی عیب‌یابی

اگر لایسنس بالا نیاید، داخل Experts log خط `STC_LICENSE` را ببین.

reasonهای مهم:

```text
license_token_parse_failed
account_mismatch
server_mismatch
expired
signature_mismatch
hidden_gate_mismatch
```

این خروجی‌ها نشان می‌دهند دقیقاً کدام input اشتباه وارد شده یا bind درست نیست.

## مرزهای قفل‌شده

این اصلاح هیچ‌کدام از این منطق‌ها را تغییر نمی‌دهد:

```text
SMT candidate logic
cycle logic
risk logic
paper entry
paper outcome
broker position manager
real auto-entry
real partial close
real hard close
validation pack
```

فقط لایه‌ی offline license و issuer tool اصلاح شده‌اند.
