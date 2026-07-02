# ENT-08 — Is invalidation the same as the stop, or can it be separate?

Section: Limit Entry, Stop, and Destination

### ENT-08 — Is invalidation the same as the stop, or can it be separate?

Why this matters: The answer determines the first execution templates and the structural labels for filled, missed, invalidated, and successful extreme entries.

Answer in these layers:
- Raw intuition: describe how you see it on the chart before formalizing it.
- Operational definition: explain how we could turn it into a field, rule, label, or policy.
- Exceptions: describe the cases where the rule fails, weakens, or changes meaning.
- Chart evidence: add examples when the idea is easier to understand visually.

Clarify these points:
- Define the exact entry location relative to the extreme zone.
- Define the stop and whether it is structural, broker-level, or both.
- Define destination selection and destination changes.
- Explain what happens before fill, after fill, and after structural change.
- Separate limit-first logic from confirmation or chase logic.

Future system outputs affected by this answer:
- entry template
- stop model
- destination model
- activation labels
- resolution labels
- cancel/replace rules

Image guidance: A chart example is strongly recommended. Mark entry, stop, invalidation, destination, and what would make the setup die.

Recommended answer folder: ../answers/ENT-08/

User answer:

