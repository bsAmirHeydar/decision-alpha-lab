# Canonical Contract Catalog

## Foundation contracts implemented now

### SchemaIdentity
Names and versions every contract. It carries namespace, name, and semantic version.

### MarketTimestamp
Carries canonical UTC epoch milliseconds plus source timezone, offset, clock ID, and precision. UTC is the ordering authority; source information preserves lineage.

### BarRecord
Represents a normalized market bar with strict OHLC geometry, volume, bid/ask, spread, source identity, and stable bar ID.

### AnatomyEvent
Represents a fact emitted by an anatomy engine at known time. It separates event time, known time, and confirmation time and carries strategy, producer, symbol, direction, reference/invalidation geometry, parent identity, cluster identity, and source hash.

### FeatureValue
Represents a typed, versioned, quality-aware value with its own known time and source lineage.

### FeatureSnapshot
Represents the immutable feature state used for a decision. It rejects duplicate feature IDs and future-known values.

### ArtifactIdentity
Provides reproducibility lineage for datasets, reports, models, and later execution artifacts.

## Reserved later contracts

CandidateTemplate, TradeCandidate, OutcomeRecord, FoldAssignment, ModelArtifact, ModelDecision, ActionPlan, ExecutionIntent, ExecutionTrace, TelemetryRecord, and PromotionDecision are intentionally deferred to their owning phases. They will reuse the primitives frozen here rather than redefine time, identity, or lineage.
