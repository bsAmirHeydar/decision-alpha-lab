# EXP0013 Astro Dashboard V7 - Visual Polish

This patch focuses on making the dashboard significantly cleaner and more visually pleasant.

## What changed

- clearer and larger titles
- bigger and more visible buttons
- more horizontal spacing between label / value / bucket / bar
- better use of the wide empty chart space
- cleaner header hierarchy
- wider cards
- more comfortable line spacing in cards and diagnostics
- compact oscillator kept clean and readable
- old dashboard objects are still force-cleaned on init / deinit / rerender

## Design goals

- make section titles obvious at first glance
- make controls immediately visible
- avoid cramped text columns
- keep the chart readable while still showing the research dashboard

## Modes

- Cockpit: 4 cards + diagnostics
- Focus: one large section + diagnostics

## Buttons

Top row:
- COCKPIT
- PATH
- MICRO
- REGIME
- MACRO
- RAW

Second row:
- TEXT ON / OFF
- OSC ON / OFF
- RELOAD

## Color logic

- low = red
- mid = yellow
- high = green
