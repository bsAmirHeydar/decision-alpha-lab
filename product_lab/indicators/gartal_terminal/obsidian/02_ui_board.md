# 02 — UI Board

## حس بصری

فضا باید شبیه cockpit معامله‌گر باشد: تاریک، تمیز، دقیق، بدون شلوغی کودکانه.

## اجزای اصلی

- Header: logo + live/cache/error
- Next Event strip
- Event table
- Filter pills
- Alert status
- Bottom timeline
- Event detail card

## Layout پیشنهادی

```text
Right Upper Dashboard
Bottom Timeline
Vertical Lines on Event Time
Small Source Status near header
```

## Hierarchy

1. Next high-impact relevant event
2. Remaining time
3. Currency/impact
4. Event title
5. actual/forecast/previous
6. filter state
7. source status

## حالت luxury

- border کم‌رنگ
- opacity کنترل‌شده
- shadow نه بیش‌ازحد
- رنگ impact قوی اما محدود
- typography منظم

## ضد شلوغی

اگر کاربر همه ارزها و همه impactها را روشن کرد، UI نباید منفجر شود. اولویت‌دهی rowها لازم است.
