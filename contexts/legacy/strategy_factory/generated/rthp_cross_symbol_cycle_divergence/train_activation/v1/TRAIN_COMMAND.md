# Train Command

Copy `configs/train_activation.real.template.v1.json` to a run-specific configuration, replace every placeholder, and run from the repository root:

```text
$env:PYTHONPATH = 'src/engine/packages'
python -m strategy_factory_rthp_train_activation_v1 validate-config --config <run-config.json>
python -m strategy_factory_rthp_train_activation_v1 run --config <run-config.json>
python -m strategy_factory_rthp_train_activation_v1 verify-run --run-root <output-root>
```

The command automatically produces all four ledgers, resolves their hashes and URIs, compiles features and labels, freezes the batch, trains all selected mature tasks with existing trainers, packages evidence, and verifies the immutable output.
