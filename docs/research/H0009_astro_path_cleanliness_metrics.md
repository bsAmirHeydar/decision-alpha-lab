# H0009 — Astro Path Cleanliness Metrics

This note defines the first Decision Alpha Lab interpretation layer for astrological data.

The project does not use astrology as a raw directional signal. It uses astrological states as causal time features for Distribution Engineering. The first target is path cleanliness: lower adverse excursion, shallower pullbacks, higher path efficiency, faster target reach, and fewer opposite-direction interruptions after an independent market execution signal.

The interpretation layer converts raw ephemeris data into seven axes:

- Flow
- Impulse
- Friction
- Pressure
- Transition
- Moon Tempo
- Saturn Drag

It then derives composite scores:

- Clean Path
- Clean Impulse
- Smooth Continuation
- Breakout Follow-through
- Pullback Risk
- Chop Risk

These scores are not trading signals. They are feature candidates. Their value must be validated by attaching them to execution outcomes and measuring MAE_R, MFE_R, pullback_depth_R, path_efficiency, clean target hit rate, and sequence lift out of sample.
