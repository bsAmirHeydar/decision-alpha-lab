# Valid Only Post F3 Rendering Policy

When valid-only view is enabled, the renderer must display only the selected post-F3 Hook candidates.

## Allowed

- selected direct structural F3H;
- selected direct 80% geometric F3H when enabled;
- selected delayed structural F3H;
- selected delayed 80% geometric F3H when enabled;
- nodes/labels belonging only to selected structural Hooks.

## Forbidden

- all other Phase02 sequences;
- same-origin siblings;
- structural fallback;
- non-selected delayed candidates;
- geometric 80% candidates when mode is structural-only.

If no post-F3 Hook qualifies, draw nothing for that F3 context.
