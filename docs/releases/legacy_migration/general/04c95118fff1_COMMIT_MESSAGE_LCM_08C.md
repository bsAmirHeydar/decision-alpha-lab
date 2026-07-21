feat(lcm): close context wave portfolio with explicit blockers

- bind the frozen LCM-08A Context portfolio and accepted LCM-08B pilot
- verify immutable source hashes for all 321 Context identities
- publish one deterministic migration packet per identity
- preserve the EXP0015 pilot as the sole parity-proven cutover-ready package
- block 320 identities with explicit owner, characterization, identity and package-boundary evidence
- publish package, parity, variance, blocker, source-lock and locator registries
- close every migration wave through non-compensatory receipts
- prove zero locator collisions, zero migrated parity failures and zero portfolio omissions
- deny consumer cutover, source lifecycle changes, quarantine and execution authority
- issue the bounded LCM-08C to LCM-09A handoff
