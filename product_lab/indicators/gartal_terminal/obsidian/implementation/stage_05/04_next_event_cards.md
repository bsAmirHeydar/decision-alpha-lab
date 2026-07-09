# Next Event Cards

## Next Event Card

Shows the nearest visible event after broker now. It includes:

- time
- currency
- impact
- countdown
- title
- actual / forecast / previous

## Next Red Card

Only shown in PRO mode. It isolates the next high-impact or red-class event. This supports traders who need risk-window awareness rather than full calendar reading.

## Rule

Cards use `store.next_event_index` and `store.next_high_index`; they do not scan independently for truth.
