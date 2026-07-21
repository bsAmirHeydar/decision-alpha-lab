# Alpha Lab LCM-13B — Controlled Consumer Wave Cutover

LCM-13B consumes the exact LCM-13A eligibility registry and applies bounded, reversible cutover in the governed reference locator plane.

## Implemented guarantees

- only the 613 consumers explicitly eligible in LCM-13A are switched;
- all 806 blocked consumers remain on their exact legacy locators;
- consumers are partitioned into bounded, dependency-aware waves;
- each wave has a plan, cutover manifest, health report, locator receipt and preverified rollback package;
- canonical resolution is primary while the legacy locator remains available as a temporary fallback;
- post-cutover mismatches are persisted separately and are never suppressed or aggregated;
- no legacy source is removed;
- no production source/configuration default is changed;
- no runtime, live-order or capital authority is created.

LCM-13C is the only permitted next phase and must rehearse rollback, forward recovery and persistent-state restoration before closure.
