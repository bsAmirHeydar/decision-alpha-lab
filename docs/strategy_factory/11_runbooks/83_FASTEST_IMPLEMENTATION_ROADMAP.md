---
type: strategy-factory-document
status: canonical
title: "Fastest Professional Implementation Roadmap"
tags:
  - strategy-factory
---

# Fastest Professional Implementation Roadmap

This roadmap turns the supplied foundation into the first complete anatomy-to-paper pipeline, then makes later anatomies plug-in work.

## Sprint 0 — merge and verify

Install the patch, run 19 Python tests, validate example manifests, compile MQL5 headers inside a small test Expert, and record any local compiler differences. No strategy logic changes.

## Sprint 1 — first adapter

Choose EXP0017 or the clearest mechanical setup. Export events/features, implement the adapter, create 20 golden fixtures, and reconcile counts with the existing engine. Target two to three days.

## Sprint 2 — candidate and outcome closure

Freeze 6–12 meaningful policy combinations, connect real bid/ask bars and cost model, materialize outcomes, and compare with hand calculations. Target two to three days.

## Sprint 3 — standard evidence

Run statistics, matched nulls, purged folds, cluster bootstrap, FDR, reality check, best-trade/cost/delay stress, and cross-feed checks. Freeze confirmation. Target three to five days depending on data.

## Sprint 4 — first AI

Train logistic/ridge baselines, then one boosted challenger and candidate ranker. Calibrate, ablate, write model card, and reject complexity without uplift. Target two to four days.

## Sprint 5 — paper

Connect live events to snapshot/candidate/model/risk/paper trace. Reconcile restart and latency. Run until enough clusters and regimes exist. Subsequent strategies reuse all of this and should require only adapter/config/fixtures.

