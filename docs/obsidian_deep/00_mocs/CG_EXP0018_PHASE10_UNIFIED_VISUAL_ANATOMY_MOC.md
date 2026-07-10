---
id: CG_EXP0018_PHASE10_UNIFIED_VISUAL_ANATOMY_MOC
project: EXP0018
phase: P10
status: implemented-evidence-package
---
# EXP0018 Phase 10 — Unified Visual Anatomy MOC

## Canonical entry
- [[docs/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/17_phase10_unified_visual_anatomy_v2/00_INDEX|P10 implementation index]]

## Core visual stack
- P08 immutable divergence lines
- Daily 18:00–17:00 frame and boundaries
- A/L/N/P Session range boxes and Q1–Q4 labels
- a1–p4 subcycle boxes, boundaries and phase labels
- 22.5-minute local micro-quarter boundaries
- explicit p4 30-minute tail
- declared 17:00–18:00 gap
- TDO and TWO finite anchors
- optional extended Session True Opens
- optional provisional week boundaries

## Concepts
- [[P10_One_Expert_Owns_The_Complete_Chart_View]]
- [[P10_Visual_Hierarchy_Mirrors_Fractal_Time]]
- [[P10_Daily_Time_Is_18_To_17_New_York]]
- [[P10_Sessions_Are_Q1_Through_Q4]]
- [[P10_Subcycles_Are_Local_Quarters]]
- [[P10_Micro_Quarters_Are_1350_Seconds_Local]]
- [[P10_P4_Is_Not_A_Ninety_Minute_Cycle]]
- [[P10_The_Declared_Gap_Is_A_Visible_Domain_State]]
- [[P10_TDO_Uses_The_L_Open]]
- [[P10_TWO_Policy_Is_Explicit]]
- [[P10_Extended_True_Opens_Are_Context_Only]]
- [[P10_Weekly_Visuals_Do_Not_Activate_WW]]
- [[P10_Object_Names_Are_Deterministic]]
- [[P10_Price_Geometry_Is_Symbol_Local]]
- [[P10_Visual_Projection_Has_No_Execution_Authority]]


## Decision maps
- [[EXP0018_P10_Unified_Source_To_Object_Map]]
- [[EXP0018_P10_Fractal_Time_Map]]
- [[EXP0018_P10_TDO_TWO_Map]]
- [[EXP0018_P10_DST_Micro_Boundary_Map]]
- [[EXP0018_P10_Object_Ownership_Map]]
- [[EXP0018_P10_Chart_Target_Map]]
- [[EXP0018_P10_Optional_Context_Gate_Map]]
- [[EXP0018_P10_Release_Gate_Map]]

## Checklists
- [[EXP0018_P10_Compile_Checklist]]
- [[EXP0018_P10_Daily_Session_Checklist]]
- [[EXP0018_P10_Subcycle_Micro_Checklist]]
- [[EXP0018_P10_TDO_TWO_Checklist]]
- [[EXP0018_P10_DST_Checklist]]
- [[EXP0018_P10_Object_Ownership_Checklist]]
- [[EXP0018_P10_Release_Checklist]]
