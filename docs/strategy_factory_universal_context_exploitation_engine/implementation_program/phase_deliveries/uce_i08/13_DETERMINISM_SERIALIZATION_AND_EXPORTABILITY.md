# Determinism, Serialization, and Exportability

Every seeded trainer is rerun with identical data, feature order, worker count, precision, and configuration. OOF and final-test evidence hashes are compared. Numeric-tolerance algorithms disclose tolerance; nondeterministic algorithms are never silently labeled deterministic.

Research serialization stores canonical trainer identity, task identity, feature order, output order, state hash, parameters, fitted summaries, and prediction fingerprints. It deliberately avoids unrestricted opaque object serialization. Runtime portability is completed in UCE-I14 through governed export.

A model can be statistically useful yet blocked from runtime when export parity is absent. Research utility and production eligibility are independent dimensions.
