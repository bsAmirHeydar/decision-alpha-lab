# EXP0013 Astro Dashboard V13 - UI Review and Redesign

## Professional UI critique of V12

1. **Header hierarchy was weak**
   - the title, metadata, status, and file info competed for the same visual attention
   - some items visually collided and reduced readability

2. **Top controls were readable but not grouped cleanly enough**
   - the navigation and utility controls needed clearer separation from the information area

3. **Card content needed a stronger internal grid**
   - labels, values, bucket text, and bars were close, so the scan rhythm was not premium enough

4. **Diagnostics panel was functional but visually under-structured**
   - it needed the same section-rule treatment and spacing discipline as the other cards

5. **Lower oscillator had unnecessary visual noise**
   - it needed to act as a clean summary strip, not a secondary clutter zone

## What V13 changes

- redesigns the header into a clearer hierarchy
- separates title, subtitle, metadata, and control rows more cleanly
- improves the internal grid of all metric cards
- adds rule separators to cards, diagnostics, and oscillator
- improves oscillator spacing and naming
- preserves minimize / expand and stable in-place refresh behavior

## Result

V13 is the current most polished cockpit build from a UI readability perspective.
