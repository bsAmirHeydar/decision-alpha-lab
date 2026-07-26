# Contract compatibility alias

Phase 17 supplies `SF01_IsTerminalSymbol` as a compatibility alias to the canonical
`SF01_IsSafeTerminalSymbol` validator. Phases 08 through 16 already reference the concise name,
while the Phase 01 codec originally exposed only the longer name. The alias has identical transport
symbol semantics and fixes terminal compilation without changing serialization, identifiers, or
runtime behavior. It belongs in the shared contract codec because all downstream MQL5 modules may
consume it.

The alias is intentionally a direct delegate rather than a second validator. This prevents policy
drift between symbol checks and keeps the Phase 01 contract source authoritative.
