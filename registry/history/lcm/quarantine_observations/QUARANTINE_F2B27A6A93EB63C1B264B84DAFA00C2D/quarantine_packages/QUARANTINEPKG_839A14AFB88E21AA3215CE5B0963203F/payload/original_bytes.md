# EXP0013 Astro Dashboard V8 - Header, Buttons, Dynamic Spacing

This patch specifically improves the three visual issues requested:

## 1) Clearer header
- larger main title
- clearer vertical separation between title, view line, CSV status, and time line
- a dedicated status badge for EXACT / FALLBACK / NOT FOUND
- better use of empty header space

## 2) Bigger buttons
- larger width and height
- more spacing between buttons
- clearer visibility in the top-right area

## 3) Better spacing inside cards
- label/value spacing is now based on the longest metric name in the section
- then extra visual gap is added after the label column
- value, bucket, and bar columns are separated more clearly
- same dynamic spacing logic is also applied to the compact oscillator

## Visual logic
- low = red
- mid = yellow
- high = green

## Cleanup
Previous dashboard objects are still force-cleared on init, rerender, and deinit.
