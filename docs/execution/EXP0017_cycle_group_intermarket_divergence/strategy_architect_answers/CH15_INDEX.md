# CH15 — Statistical Reporting, Metric Language, and Actionable Signal Dataset

## Chapter role

Chapter 15 defines the reporting language of EXP0017.  
The previous chapters defined what a valid divergence is, how cycle groups are treated, when a signal is confirmed, how clean-symbol execution is understood, and how uncertainty remains suspended until statistics speak.  
This chapter turns that doctrine into a statistical reporting field: what is worth measuring, what belongs in the sample, what must be removed from the language, and how signals should be compared without contaminating the base model.

## Strategy-architect answers captured

1. The important statistical measures are the measures already defined so far: win rate, risk-to-reward, profit in pips, profit in pips divided by total market movement in pips, cycle-group overlap, signal count per day, per week, per month, and related measures.
2. Only valid signals that became tradeable are part of the main sample: the target candle must close and confirm the divergence.
3. Non-actionable or unconfirmed events do not need to enter the main statistical population at this stage.
4. The cycle-group type is mandatory in the report and is essential for statistical samples.
5. For unresolved reporting details, the recommended analytical structure should be used.
6. For unresolved grouping and comparison details, the recommended analytical structure should be used.
7. Emotional concepts must be removed; an expert has no emotion.
8. All fields described so far are valuable, and additional useful statistical ideas may be added.
9. For unresolved normalization choices, the recommended analytical structure should be used.
10. For unresolved future reporting layers, the recommended analytical structure should be used.

## Core doctrine

The statistical report is not a decorative summary. It is the place where the strategy stops being a visual idea and becomes measurable behavior.

The base sample must focus on confirmed, tradeable signals. A raw touch is not enough. A possible divergence is not enough. The confirmation candle must close, the divergence must remain valid, and the signal must reach the stage where it could be traded under the strategy rules.

The report must preserve every important identity of the signal:

- cycle group
- direction
- hunter symbol
- clean symbol
- reference family
- time window
- confirmation time
- entry assumption
- stop basis
- cycle-end result
- maximum later reward potential
- pip movement
- normalized movement against the day
- dollar outcome
- overlap with other cycle groups
- frequency in day, week, and month

## Files in this chapter

- `CH15_statistical_reporting_and_metric_language_doctrine.md`
- `CH15_research_translation_and_statistical_mission.md`
- `CH15_actionable_signal_dataset_boundary.md`
- `CH15_metric_catalog_and_recommended_fields.md`
- `CH15_hypothesis_register.md`
- `CH15_glossary_and_language.md`

## Obsidian concepts added

- `CG_Chapter_15_Statistical_Reporting_Doctrine`
- `Actionable_Confirmed_Signals_Only`
- `Metric_Family_For_CG_Divergence`
- `Pip_Movement_And_Daily_Range_Normalization`
- `Cycle_Group_Type_As_Mandatory_Report_Field`
- `Cycle_Group_Overlap_As_Statistical_Field`
- `Signal_Frequency_Per_Day_Week_Month`
- `No_Emotional_Language_In_Expert_Reports`
- `Recommended_Metrics_When_Strategy_Architect_Is_Uncertain`
- `Statistical_Report_As_Strategy_Memory`

## Output principle

The reporting layer must support later decisions, but it must not decide too early.  
The report records the world of confirmed signals. Statistics then reveal which parts of that world deserve priority, filtering, risk adjustment, or AI scoring.
