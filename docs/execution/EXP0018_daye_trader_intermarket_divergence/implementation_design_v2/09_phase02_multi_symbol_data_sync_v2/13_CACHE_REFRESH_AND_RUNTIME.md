---
id: EXP0018-P02-CACHE-REFRESH
title: "P02 Cache and Refresh Runtime"
type: runtime-design
status: active
project: EXP0018
---
# Refresh و cache

در هر timer ابتدا فقط latest closed bar time با `CopyTime` probe می‌شود. Full `CopyRates` زمانی انجام می‌شود که:

- engine هنوز ready نیست
- latest bar یکی از symbolها تغییر کرده
- force-refresh interval رسیده

این طراحی از full-history rescan در هر tick جلوگیری می‌کند. History-not-ready عمداً retry می‌شود.
