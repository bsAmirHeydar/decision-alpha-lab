# Strategy Factory

`lab/11_strategy_factory` is the shared anatomy-to-research-to-execution engine
for Decision Alpha Lab. Strategy-specific code is restricted to:

1. an anatomy adapter;
2. strategy-specific feature providers;
3. candidate policy plugins where the built-ins are insufficient;
4. a versioned JSON manifest.

All official statistics, anti-overfit controls, model training, paper execution,
risk gating, artifacts, and promotion states are shared.

Start with:

```powershell
python .\lab\11_strategy_factory\sf.py validate-manifest `
  .\lab\11_strategy_factory\examples\manifests\temporal_divergence.json
```

Canonical documentation: `docs/alpha_lab_master_architecture/strategy_factory/00_start_here/00_STRATEGY_FACTORY_MOC.md`.
