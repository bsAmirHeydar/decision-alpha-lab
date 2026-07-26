# Level 08 STC SMT Risk Plan and Paper Entry

Level 08 adds the no-order paper entry model for EXEC001 STC SMT Cycles.

It converts confirmed Level 07 signals into paper trade plans using:

- next-check open entry
- selected reference W stop
- Final Reward R target
- equity and risk percent sizing
- broker tick value when available
- shared Contract Size fallback otherwise
- broker min/max/step audit
- max three paper entries per M
- Hedging OFF direction lock per M

No real order is sent. No partial close, hard close, drawing, or outcome simulation is performed in this level.

Main output:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level08_paper_entries.csv`
