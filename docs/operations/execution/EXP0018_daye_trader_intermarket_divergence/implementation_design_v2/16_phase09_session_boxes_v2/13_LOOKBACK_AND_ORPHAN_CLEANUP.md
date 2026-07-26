# Lookback and Orphan Cleanup

`InpLookbackWeeks` limits admitted sessions by UTC session start. Default is two weeks. The P03 source request must be large enough to cover the desired interval.

When cleanup is enabled, owned P09 boxes no longer represented by an admitted source snapshot inside lookback are deleted. Cleanup remains restricted to configured symbol charts and the P09 prefix. Deinitialization cleanup is disabled by default.
