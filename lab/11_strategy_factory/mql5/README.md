# MQL5 Strategy Factory bridge

The headers in this directory define the shared contracts used by all future
MQL5 anatomy adapters and execution bridges. They are intentionally free of
strategy doctrine. A strategy-specific Expert Advisor should:

1. build an `SF_AnatomyEvent` from its existing deterministic engine;
2. validate all features against the closed-bar decision timestamp;
3. generate or receive an approved `SF_TradeCandidate`;
4. pass the intent through `SF_RiskGate`;
5. use `CSF_PaperBroker` until a separately promoted live bridge is approved.

No header in this patch calls `OrderSend`, `OrderCheck`, or `CTrade`.
