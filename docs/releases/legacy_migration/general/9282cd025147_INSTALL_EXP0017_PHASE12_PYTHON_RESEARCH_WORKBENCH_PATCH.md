# Install — EXP0017 Phase 12 Python Research Workbench Patch

This patch adds Phase 12 for EXP0017: MQL5 research bridge, Python research workbench, experiment registry template, documentation, and Obsidian notes.

Compile:

`mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Python_Research_Bridge_Anatomy.mq5`

Run Python from repository root:

```powershell
python .
esearch\exp0017_phase12\python\phase12_research_workbench.py --data-dir . --out-dir .
esearch\exp0017_phase12\outputs
```

Boundary: no trading, no execution, no strategy mutation.
