feat(alpha-lab): add shared anatomy-to-execution strategy factory

Add a reusable Strategy Factory that converts any approved market anatomy into
canonical events, immutable feature snapshots, bounded entry/stop/exit
candidates, causal outcome simulation, standard statistics, anti-overfit
validation, model training and ranking, paper execution, hard risk gates,
execution contracts, promotion governance, Obsidian documentation, templates,
examples, schemas, MQL5 bridge headers, and automated tests.

The patch keeps strategy-specific work limited to anatomy adapters, feature
providers, policy plugins, manifests, and fixtures. It intentionally introduces
no live order-send authority.
