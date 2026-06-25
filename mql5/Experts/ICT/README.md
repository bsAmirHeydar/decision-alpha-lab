# ICT Experts

## ICT001_SweepIFVGCISDExecutor

Batch expert for EXP0014 ICT:

L-node sweep -> FVG in sweep path -> IFVG -> CISD -> RR filter -> CSV journal.

The expert is intentionally not tick-driven. `OnTick()` is empty. By default it runs once on init, writes CSV files, and removes itself.
