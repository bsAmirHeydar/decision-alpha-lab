# EXP0017 — Statistical Field Catalog

## هدف سند

این سند فهرست میدان‌هایی را مشخص می‌کند که از روز اول باید در حافظه آماری و گزارش‌ها در نظر گرفته شوند تا بعداً برای تست، رتبه‌بندی، مدل‌سازی و AI داده ناقص نداشته باشیم.

## 1. شناسه سیگنال

- signal_id
- trading_day_ny
- broker_date
- confirmation_time_ny
- confirmation_time_broker
- chart_timeframe
- signal_status

## 2. سایکل‌گروپ

- cg_name
- cg_minutes
- current_cycle_index
- current_cycle_start_ny
- current_cycle_end_ny
- current_cycle_position_in_day
- time_to_cycle_end_at_confirmation

## 3. مرجع

- reference_cycle_index
- reference_cycle_start_ny
- reference_cycle_end_ny
- reference_distance
- reference_side: high/low
- hunter_reference_price
- clean_reference_price
- reference_fresh_at_signal
- reference_invalidated_after_signal

## 4. نمادها

- symbol_a
- symbol_b
- hunter_symbol
- clean_symbol
- hunter_side
- clean_side
- direction: buy/sell

## 5. هانت

- hunt_time_ny
- hunt_time_broker
- hunt_candle_open_time
- hunt_price
- hunt_type_base: touch_or_break
- exact_touch_flag
- break_depth_points
- break_depth_pips

نکته: break depth فعلاً فیلتر نیست، فقط field آماری است.

## 6. تایید

- confirmation_candle_open
- confirmation_candle_close
- confirmed_after_close
- valid_at_confirmation
- invalidated_at_confirmation
- entry_permission_time

## 7. سشن و زمان

- cash_session_flag
- minutes_from_cash_open
- minutes_to_cash_close
- day_segment_descriptive
- news_flag_optional_later

خبر فعلاً فیلتر نیست. اگر ثبت شود فقط برای مطالعه جانبی است.

## 8. overlap و تراکم

- total_cg_overlap_count
- same_direction_overlap_count
- opposite_direction_overlap_count
- same_symbol_overlap_count
- hedge_overlap_flag
- signal_count_today
- signal_count_this_cg_today
- signal_count_this_week
- signal_count_this_month

## 9. ورود و ریسک

- intended_entry_symbol
- intended_entry_direction
- estimated_entry_price
- stop_price
- stop_distance_points
- stop_distance_pips
- fixed_risk_percent
- risk_money

## 10. خروج‌های زمانی و نتیجه

- cycle_end_exit_price
- outcome_at_cycle_end_pips
- outcome_at_cycle_end_r
- outcome_at_cycle_end_money
- day_end_exit_price
- outcome_at_day_end_pips
- outcome_at_day_end_r
- outcome_at_day_end_money

## 11. چندپنجره بعدی

- outcome_after_1_cycle
- outcome_after_2_cycles
- outcome_after_3_cycles
- outcome_after_n_minutes
- maximum_intraday_reward_r
- maximum_intraday_reward_pips
- maximum_intraday_adverse_r
- maximum_intraday_adverse_pips
- giveback_after_mfe

## 12. نرمال‌سازی

- clean_symbol_daily_range_pips
- pip_outcome_divided_by_daily_range
- mfe_divided_by_daily_range
- mae_divided_by_daily_range

## 13. ابطال

- invalidated_after_confirmation
- invalidation_time
- invalidation_candle
- invalidation_before_stop
- invalidation_after_stop
- double_hunt_flag

## 14. کیفیت آماری بعدی

- win_loss_flag
- stopped_flag
- stop_streak_context
- cg_family_rank_later
- quality_score_later

این فیلدهای رتبه و کیفیت در نسخه خام نباید تصمیم بسازند. فقط بعداً با مدل پر می‌شوند.
