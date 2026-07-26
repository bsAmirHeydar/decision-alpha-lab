# 09 - Owner Decisions Pass 1

This document records the first owner clarification pass for EXEC001 STC SMT Cycles.

## Locked decisions

1. No entries are allowed in the temporal gaps between M cycles.
2. Gap data is not required for signal detection, but open positions must still be managed if final TP or SL is reached.
3. W high and W low are the high and low of a synthetic 90-minute candle. The timeframe used to build them does not change the final high/low if data is complete.
4. W2 can compare only with W1.
5. W3 can compare only with W2 and W1.
6. W4 can compare only with W3, W2, and W1.
7. No W compares with itself.
8. W1 gives no signal.
9. Hunts use no tolerance.
10. Buy and sell side mapping from SMT was confirmed.
11. Each symbol has its own W levels. The comparison is structural, not shared-price.
12. If the clean symbol also hunts before check-candle close, the divergence disappears and no entry is allowed.
13. The close of the same check candle is enough for confirmation.
14. Only one entry is allowed per signal. Persistent divergence in later check candles does not create another entry.
15. The last check candle of an M is not tradable. It is reserved for partial or hard close.
16. If buy and sell occur in the same check candle, no trade is opened.
17. Max trades per M is total across both symbols.
18. The trade counter increments only after a position is opened.
19. Hedging direction lock is direction-based, not symbol-based.
20. When Hedging is ON, both buy and sell are allowed inside an M, but not if they confirm in the same check candle.
21. Spread is not used as an entry filter.
22. Stop uses the reference W of the trade symbol.
23. Final Reward 10 means 10R.
24. Tick value should be used when available. Contract Size is fallback.
25. Broker min/max volume constraints must be respected live.
26. Partial timing is at W4 end.
27. M3 partial is meaningless because hard close dominates.
28. Partial applies even if the position is in loss.
29. Partial volume is rounded upward.
30. A trade can be partialed only once.
31. Everything must be closed after 15:30 New York.
32. Previous STC trading-day data must not affect today's decisions.
33. Restart inside the current STC day may reconstruct state from current-day data and account positions.
34. Entry OFF means audit only; no trade.
35. The EA can be attached to either of the two index charts because chart symbol is irrelevant.
36. Check candles should be internally aggregated.
37. Backtest uses open of the next check candle for entry.
38. Use check-candle timeframe for backtest outcome.
39. Include spread and commission reporting.
40. No trade when data is missing or market is closed.
41. The same logic applies to NDX/NQ/NAS100 equivalents.
