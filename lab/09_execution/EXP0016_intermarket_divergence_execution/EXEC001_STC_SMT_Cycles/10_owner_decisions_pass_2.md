# 10 - Owner Decisions Pass 2

This document records the second owner clarification pass for EXEC001 STC SMT Cycles.

## Locked decisions

1. Equality counts as touch.
2. If SL or TP is reached during an M gap, normal position management applies.
3. No new entries or detections occur in gaps.
4. Partial happens exactly at W4 end.
5. Missed partial must be performed later at the first opportunity if the position is still open and not already partialed.
6. Missed partial is performed even if the system is already in a later M.
7. M3 partial can be disabled because hard close dominates.
8. If hard close is missed, it must be performed at the first opportunity.
9. Backtest entry uses the open of the next check candle.
10. Check candles are anchored from 20:00 New York.
11. The final check candle of each M cannot produce entry.
12. If multiple valid references exist, select the reference that produces the largest stop distance on the clean traded symbol.
13. If multiple references exist for the same side, the selected reference is the largest-stop reference for the clean symbol.
14. If buy and sell confirm in the same check candle, the event is forgotten/discarded and no trade is opened.
15. Entry OFF means no entry and no delayed entry.
16. If the EA is offline at the exact entry time, no later entry is allowed.
17. If order send fails, the signal is consumed and trade counter is not incremented.
18. Hedging scope is per M. Opposite directions are allowed in later M cycles even when Hedging is OFF.
19. Each M allows at most three trades.
20. If calculated volume is above broker max, the system may split orders.
21. Contract Size is shared.
22. TP is calculated without transaction costs.
23. Spread and commission are read from broker/data for reporting when possible.
24. If a post-entry check candle hits both SL and TP, the outcome is `AMBIGUOUS`.
25. Outcome is evaluated with the check-candle timeframe.
26. Both symbols must have complete data for trading decisions.
27. Restart persistence should use current-day candles, journal state, and magic-number positions.
28. Duplicate EA instances must be blocked.
29. Symbol1 and Symbol2 are both data and execution symbols.
30. Drawing is required and can be designed without further owner questions.
31. Output journals should be designed by the implementation logic.
32. Build order should start with research and paper runtime before auto-trade.
33. Hard-close retry must repeat every configured number of seconds until complete.
34. The EA manages only positions with its own magic number.
35. Current STC trading day means data after the STC day start, not calendar midnight.
