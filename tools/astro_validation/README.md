# Astro Signal Validator

This tool audits the astro-only paper journals produced by the execution families.

## Research runner

You can now generate those journals directly from a raw astro feature CSV, without waiting for MT5 execution:

```bash
python tools/astro_validation/astro_paper_family_runner.py ^
  --csv lab/03_experiments/EXP0013_astro_feature_store/sample.csv ^
  --family A0001 ^
  --out-journal lab/03_experiments/EXP0013_astro_feature_store/paper/a0001_journal.csv ^
  --config tools/astro_feature_builder/astro_config.example.json
```

Supported families:

- `A0001` transit trend pulse
- `A0002` natal resonance
- `A0003` friction polarity
- `A0090` live shell doctrine profile in paper form

The runner stays astro-only:

- raw feature CSV in
- pure astro timing stack and score surface
- family gates and state machine
- paper journal out

That journal can then be validated with the validator below.

## What it checks

- doctrine and schema stability
- phase / action distribution
- direction and regime balance
- macro / meso / micro / minute timing averages
- hold-duration profile
- threshold sensitivity grid
- shuffled baseline on the action stream

## Example

```bash
python tools/astro_validation/astro_signal_validator.py ^
  --journal lab/03_experiments/EXP0013_astro_feature_store/paper/a0001_journal.csv ^
  --out-json lab/03_experiments/EXP0013_astro_feature_store/validation/a0001_report.json
```

The output is a JSON report so each family can be reviewed, promoted, or rejected without mixing in discretionary interpretation.
