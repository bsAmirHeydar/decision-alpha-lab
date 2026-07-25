feat(lcm): implement 13C rollback rehearsal and cutover closure

- rehearse exact rollback and deterministic forward recovery for all 27 waves
- account for six persistent-state planes per wave
- bind prior and canonical locators to immutable evidence digests
- close 613 cutover consumers with explicit residual risk
- retain 806 blocked legacy consumers unchanged
- hand deprecation candidates to LCM-14A without quarantine or deletion authority
