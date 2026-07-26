# AnatomyEvent Contract

An AnatomyEvent is a market fact, not a trade. It answers: what happened, when did it happen, when was it knowable, and who produced the claim?

## Core fields

Strategy and producer IDs/version, primary and reference symbol, direction, event/known/confirmation times, reference and invalidation prices, timeframe, session, parent event, market-event cluster, source hash, and anatomy state.

## Event identity

The ID includes strategy identity, symbols, direction, all three times, timeframe, parent event, cluster, and source hash. It does not include outcome, model score, later feature state, or execution result.

## Cluster identity

`market_event_cluster_id` groups multiple rows that arise from the same underlying market occurrence across cycle groups, timeframes, strategies, or entry policies. Later fold splitting and portfolio risk use this field to avoid false independence.

## Validation

Events with no direction, invalid identifiers, non-finite geometry, nonpositive timeframe, missing cluster, wrong time order, or mismatched stable ID are rejected. The contract does not decide whether an event is economically useful.
