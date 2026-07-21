# SAED V4-38 — Immutable Runtime and MQL5 Parity

This patch adds the complete V4-38 research reference: closed ABIs, hermetic compilation, immutable runtime bundle, integrity manifests, generated MQL5 static runtime, deterministic parity vectors, Python and MQL5 semantic runners, state replay, external-evidence separation, release gates, governance and bounded V4-39 handoff.

Validation:

`python tools/strategy_factory/saed_v4_38/run_saed_v4_38_full_qa.py`

`python tools/strategy_factory/saed_v4_38/validate_saed_v4_38_delivery.py`

Actual MetaEditor compilation and MT5 Terminal parity remain pending external evidence. The patch cannot submit orders, activate capital or authorize production.
