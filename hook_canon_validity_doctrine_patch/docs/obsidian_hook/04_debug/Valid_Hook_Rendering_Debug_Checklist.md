# Valid Hook Rendering Debug Checklist

Use this when valid-only mode is enabled but the chart still shows too many Hooks or no Hooks.

## Check 1 — visible set

Verify that `visible_hook_groups` contains only:

- Hook After Opposing F3;
- Hook After Hook child;
- parent companion of Hook-after-Hook child.

## Check 2 — draw path

Every draw path must filter by `visible_hook_groups`.

Check:

- cycle arc renderer;
- sequence label renderer;
- node label renderer;
- envelope renderer;
- diagnostic overlays.

## Check 3 — fallback

Production valid-only mode must not enable structural fallback.

## Check 4 — stale objects

Old Hook objects must be removed before drawing the new view.
