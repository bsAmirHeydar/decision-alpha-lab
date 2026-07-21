# Lifecycle Contract

The canonical lifecycle is INITIALIZE, HISTORICAL_BACKFILL, INCREMENTAL_UPDATE, RESTART_RECONCILE, CHART_CHANGE_RECONCILE and OWNED_CLEANUP. Restart must be idempotent under canonical IDs. Historical backfill and incremental update must consume the same event semantics. Deinitialization may delete only the canonical instance namespace.

Missing cleanup evidence and broad deletion are blockers. The contract does not pretend legacy code already meets the canonical lifecycle.
