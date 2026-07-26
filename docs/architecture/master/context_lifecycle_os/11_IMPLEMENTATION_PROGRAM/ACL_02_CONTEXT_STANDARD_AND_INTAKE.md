---
title: ACL-02 Context Standard and Intake
status: accepted-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, implementation-program, acl-02]
---
# ACL-02 Context Standard and Intake

ACL-02 operationalizes the Context definition boundary. It introduces a complete package contract, interview catalog, scaffold, closed schemas, missingness and ambiguity analysis, causal-clock validation, semantic consistency checks, security classification, authority binding and generated readiness reporting.

## State boundary

Input: `DRAFT_CONTEXT`. Output: `INTAKE_COMPLETE`, `SEMANTIC_REVIEW_REQUIRED`, or—after a separate ACL-00 approval—`SEMANTICALLY_VALIDATED`. ACL-02 never compiles detectors or enters research.

## Operator commands

```powershell
python -m src.engine.tooling.strategy_factory.acl_os.acl_02.cli scaffold CTX_EXAMPLE
python -m src.engine.tooling.strategy_factory.acl_os.acl_02.cli questions CTX_EXAMPLE
python -m src.engine.tooling.strategy_factory.acl_os.acl_02.cli evaluate lab/11_strategy_factory/contexts/CTX_EXAMPLE --permit permit.json --output-dir reports/acl02
```

## Delivery

- [[00_MOC]]
- [[ACL_02_STATUS]]
- [[ACL_03_CONTEXT_COMPILER_AND_ONBOARDING]]
