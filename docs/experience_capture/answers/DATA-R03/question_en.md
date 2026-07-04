# DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity

## Question

How should NDS training be organized so that learned knowledge becomes stable infrastructure, instead of starting from zero every time? How should context, zone, and entry be trained layer by layer?

## Why This Question Remains

The NDS anatomy has already become a structural foundation. The AI training process should follow the same pattern: train one layer, consolidate what was learned, make it inspectable and reusable, then use that knowledge as infrastructure for the next layer. This prevents the system from repeatedly re-learning the same problems and allows each trained component to become capital.

## Answer Requirements

Please clarify:

- Should training be staged layer by layer?
- Which layer should be trained first?
- Should context, zone, and entry be trained separately?
- Which layers are fractal?
- Should the entry layer be single-timeframe rather than fractal?
- How should learned knowledge become stable and reusable?
- How should the user inspect and correct what the model learned?
- Should future layers depend on frozen/validated knowledge from previous layers?
- How should algorithms be optimized and reviewed?
- What should the final output model contain?

## Expected Output

```text
layered_training_curriculum_v1
context_training_stage_v1
zone_training_stage_v1
entry_training_stage_v1
trained_knowledge_registry_v1
knowledge_consolidation_policy_v1
human_inspection_training_report_v1
layer_dependency_model_v1
```
