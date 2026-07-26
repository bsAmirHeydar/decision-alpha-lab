---
id: EXP0018-P05-PAIR-STATE
title: "P05 Pair State Model"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Pair State Model

| A | B | State | Meaning |
|---|---|---|---|
| false | false | NONE | no symbol has touched its own reference |
| true | false | A_ONLY | A is Hunter, B is Protected |
| false | true | B_ONLY | B is Hunter, A is Protected |
| true | true | BOTH | double touch; not one-sided |
| unavailable | any | UNAVAILABLE | no valid classification |

`A_ONLY` and `B_ONLY` are candidate facts for P06. They are not confirmed signals.
