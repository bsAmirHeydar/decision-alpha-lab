# Install EXP0018 Phase 11 Historical Replay v2

1. Extract at repository root.
2. Run the Phase 11 PowerShell checks.
3. Compile `mql5/Experts/DayeTrader/EXP0018_Daye_Historical_Replay_Anatomy.mq5`.
4. Configure exact broker symbols and a manual fixed broker UTC offset.
5. Select a bounded New York replay range and attach the Expert.
6. Read outputs from MetaTrader Common Files.

The Expert reconstructs history only and has no trading authority.
