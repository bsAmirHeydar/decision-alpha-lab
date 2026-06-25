# Astro Signal Validator

This tool audits the astro-only paper journals produced by the execution families.

## What it checks

- doctrine and schema stability
- phase / action distribution
- direction and regime balance
- hold-duration profile
- threshold sensitivity grid
- shuffled baseline on the action stream

## Example

```bash
python tools/astro_validation/astro_signal_validator.py ^
  --journal "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro\paper\a0001_transit_trend_pulse.csv" ^
  --out-json lab/03_experiments/EXP0013_astro_feature_store/validation/a0001_report.json
```

The output is a JSON report so each family can be reviewed, promoted, or rejected without mixing in discretionary interpretation.
