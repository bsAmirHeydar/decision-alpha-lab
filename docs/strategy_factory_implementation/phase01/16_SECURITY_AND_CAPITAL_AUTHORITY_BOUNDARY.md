# Security and Capital Authority Boundary

No Phase 01 file may submit, check, modify, or cancel a live order. The static tests search for order-authority tokens in the contract package.

## Authority separation

- AnatomyEvent: market-description authority.
- FeatureSnapshot: context-description authority.
- ModelDecision, later: recommendation authority.
- Risk engine, later: rejection and reduction authority.
- Broker adapter, later: request-construction authority.
- Live order sender: separately enabled deployment authority.

## Data trust

A valid schema does not mean a trusted source. Producer IDs, versions, source hashes, and artifact lineage support later allowlists and signature verification. Unrecognized producers must be rejected or quarantined.
