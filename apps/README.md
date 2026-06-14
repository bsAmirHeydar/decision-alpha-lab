# Apps

This directory contains user-facing applications built on top of the Decision Alpha Lab research engine.

The apps layer must stay separate from `lab/`.

```text
apps/
├── api/   # FastAPI backend for UI and tooling
└── web/   # React visual research terminal
```

---

## Boundary

Apps may:

- read research outputs
- request approved metric runs
- visualize candles, nodes, metrics, experiments, validations
- expose typed APIs

Apps must not:

- redefine market logic
- duplicate metric logic
- decide hypothesis validity
- bypass validation
- embed execution rules into UI code

---

## Development Order

1. API read endpoints
2. visualization contracts
3. frontend shell
4. replay core
5. M0001 visual adapter
6. research lineage browser
7. validation workbench
