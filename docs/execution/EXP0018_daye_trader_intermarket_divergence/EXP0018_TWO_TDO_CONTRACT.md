# قرارداد TWO و TDO

## TWO — Tuesday Weekly Open

- Anchor time: سه‌شنبه 18:00 نیویورک
- Anchor price: open اولین داده معتبر در آن زمان
- Start: همان timestamp
- End: پایان جمعه همان هفته
- Type: horizontal segment
- Default visible: ON
- Default color: Red
- Inputs: on/off, width, color

## TDO — Trading Day Open

- Anchor time: 00:00 نیویورک، شروع L
- Anchor price: open همان زمان
- Start: 00:00
- End: 16:59:59 همان روز معاملاتی
- Type: horizontal segment
- Default visible: ON
- Default color: Red
- Inputs: on/off, width, color

## نکات داده‌ای

اگر bar دقیقاً روی anchor timestamp وجود نداشته باشد، تعریف «اولین bar معتبر داخل بازه» یا روش interpolation باید پیش از کدنویسی تصویب شود.
