# FlagCountingVNext

FlagCountingVNext is the clean implementation layer for the final F-counting grammar.

The rendering layer must follow:

`docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC.md`

Core visualization rules:

- render body only by default,
- draw `Origin -> Leg1` as a straight line,
- draw `Leg1 -> Waist -> Leg2` as a clean curve,
- show `F1/F2/F3` as tiny labels,
- show internal `1/2` as tiny numeric labels only,
- use four colors for direction and live/confirmed status,
- draw higher scale with stronger line width and larger labels,
- stack labels vertically so they do not collide,
- hide debug overlays by default.
