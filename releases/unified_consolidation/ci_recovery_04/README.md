# UC04 Historical Release Integrity Recovery 01

## Intent

Remove the systemic CI failure caused by treating the accepted UC04-W0 patch snapshot as a permanent byte lock on all active source files.

## Scope

This patch introduces a reusable historical-release integrity service and changes the W0 verifier to distinguish:

- immutable stage evidence;
- evolvable active implementation and tests;
- separately governed semantic baseline freezes.

Text hashes are checkout-portable across LF and CRLF. Immutable evidence corrections use an append-only, generically discovered amendment chain. The original W0 ledger is not rewritten.

## Non-goals

No MQL5 consumer, market-data contract, RTHP doctrine, feature, label, model, execution rule, order authority or capital authority changes.

## Expected result

The existing UC04 Semantic Foundation and UC04 W1B Native Qualification workflows can rerun the W0 verifier after legitimate active-tool evolution without historical self-hash failures. Immutable W0 evidence still fails closed on unauthorized content changes.
