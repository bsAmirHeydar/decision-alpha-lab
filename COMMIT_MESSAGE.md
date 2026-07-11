fix(alpha-lab): repair SF04 and SF05 MQL5 serialization compatibility

Replace unsupported LongToString calls with the repository-approved IntegerToString pattern across the Phase 04 plugin registry and Phase 05 runtime generation/result sink layers, preserving canonical serialization semantics and restoring the Engineering Policy check.
