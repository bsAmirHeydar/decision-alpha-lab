# NDS Pre-Canon Audit Report

## Scope

This audit covered the current NDS Hook/Zone knowledge and implementation surface before final questionnaire capture.

### Indexed corpus

| Corpus | Files indexed |
|---|---:|
| `docs/nds_hook_architecture` | 77 |
| `docs/hook_validity` | 6 |
| `docs/obsidian_hook` | 121 |
| `docs/flag_counting` | 144 |
| `docs/experience_capture` | 335 |
| `FP_Hook*.mqh` implementation modules | 53 |

The deep authority review focused on the Hook Canon phases, Hook validity doctrine, current Obsidian Hook policies, Phase01–10 implementation chain and the central Phoenix EA.

## Baseline conclusion

The project has a coherent layered NDS infrastructure, but parts of the latest Post-F3 implementation were more confident than the unresolved Canon permits. The correct pre-questionnaire action is therefore:

1. fix mechanical/contract defects;
2. improve auditability;
3. preserve current behavior behind explicit inputs;
4. document semantic gaps;
5. avoid inventing Zone or final ownership rules.

## Locked and safe to enforce now

| Contract | State |
|---|---|
| canonical valid-only visible set | retained |
| Hook-after-Hook parent/child lineage | retained |
| death before terminal confirmation means non-Hook | retained |
| finite post-F3 ownership | retained |
| structural bar-index authority | enforced |
| no broker execution in Hook Phase02 | enforced |
| Zone implementation deferred | retained |

## Corrected defects

| Defect | Correction |
|---|---|
| post-F3 bar count converted to wall-clock seconds | use canonical bar-index distance |
| direction strictness input ignored | input now controls filter; strict remains default |
| `EARLIEST_FIRST` did not select earliest first | origin bar comparison moved ahead of directness |
| 0/1 point tolerance silently became 2 | exact configured tolerance honored |
| selected F3 terminal evidence lost | stored on sequence and exported |
| effective recognition contract absent from audit | added to summary CSV and log |

## Open semantic debt

| Area | Why it remains open |
|---|---|
| ownership-window number | questionnaire explicitly requests user decision |
| ownership termination events | not fully specified |
| delayed/rebound proof | current code only infers “not direct” |
| geometric 80% denominator | not canonically defined |
| wick versus close | not canonically defined |
| confirmation count | not canonically defined across timeframes |
| closed Hook after later origin breach | history/production/Zone split unresolved |
| Zone anatomy and lifecycle | intentionally not yet implemented |

## Patch policy

This is a minimal safe stabilization patch. It does not refactor unrelated Hook phases, alter Rally behavior, add trading execution, or convert draft Zone material into code.
