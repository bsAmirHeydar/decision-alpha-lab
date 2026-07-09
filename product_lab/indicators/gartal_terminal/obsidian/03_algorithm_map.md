# 03 — Algorithm Map

## Flow

```text
Fetch → Parse → Normalize → Filter → Relevance → Render → Alert
```

## مهم‌ترین اصل

UI به source وابسته نیست. source فقط event نرمال‌شده تحویل می‌دهد.

## Entity اصلی

`GT_NewsEvent`

## States

- upcoming
- active window
- released
- past
- stale
- source failed

## Alert State

هر event چند threshold دارد. هر threshold فقط یکبار alert می‌دهد.

## Time Model

```text
source time → UTC → broker time → chart time
```

## Object Model

هر object با prefix `GT_` ساخته می‌شود و در deinit پاک می‌شود.
