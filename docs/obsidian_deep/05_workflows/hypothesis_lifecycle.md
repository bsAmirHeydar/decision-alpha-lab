
---
type: workflow
---

# Hypothesis Lifecycle

## وضعیت‌ها

| Status | معنی |
|---|---|
| `raw` | ایده خام |
| `specified` | claim و metric مشخص شده |
| `experimenting` | در حال تست |
| `inconclusive` | نتیجه ناکافی |
| `rejected` | رد شده اما قابل یادگیری |
| `validated_local` | روی یک بخش جواب داده |
| `validated_multi_regime` | روی regimeهای مختلف مقاوم بوده |
| `production_candidate` | آماده paper/live shadow |
| `archived` | بسته شده |

## شرط انتقال

هیچ hypothesis از `raw` به `experimenting` نمی‌رود مگر اینکه failure condition داشته باشد.
