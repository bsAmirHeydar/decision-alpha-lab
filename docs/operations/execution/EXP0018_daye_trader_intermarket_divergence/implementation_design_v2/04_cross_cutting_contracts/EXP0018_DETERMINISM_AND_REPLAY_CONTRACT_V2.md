  ---
  id: EXP0018-REPLAY-CONTRACT-V2
  title: "قرارداد Determinism و Replay v2"
  type: contract
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---
# قرارداد Determinism و Replay v2

- live و replay یک engine و transition table دارند.
- replay فقط eventهای در دسترس تا cursor را می‌بیند.
- event ordering canonical است.
- نتیجه با event hash و golden ledger مقایسه می‌شود.
