# Performance and refresh

Stores are bounded by inputs. Processed result IDs prevent repeated work. Reference matching is linear in reference and current observation counts; current expected cardinality is small. Future optimization may add a composite-key index without changing identities or behavior.
