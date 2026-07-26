  ---
  id: EXP0018-RELEASE-GATES-V2
  title: "EXP0018 Release Gate Matrix v2"
  type: quality-gate
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# Release Gates

| Gate | Evidence | Failure action |
|---|---|---|
| Doctrine | ADR + examples | stop |
| Compile | 0 errors/0 warnings | hotfix |
| Contract | validators/tests | stop |
| Replay | event hash parity | causal debug |
| Visual | supervisor golden pass | renderer/detector triage |
| Data | no orphan/duplicate | producer repair |
| Performance | budget pass | optimize without semantic change |
| Rollback | drill pass | no release |
| Authority | no order API | critical stop |
