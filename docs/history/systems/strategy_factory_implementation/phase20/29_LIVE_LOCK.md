# Live Lock

`live_authority` is a configuration field constrained to false. The integration package contains no `OrderSend`, `OrderCheck`, `CTrade`, position close, or asynchronous order API. Any attempt to introduce those tokens fails the Phase 20 boundary guard.
