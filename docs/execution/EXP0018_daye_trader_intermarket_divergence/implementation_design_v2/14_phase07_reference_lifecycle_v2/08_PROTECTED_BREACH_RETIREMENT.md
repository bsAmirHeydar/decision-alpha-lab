# Protected-breach retirement

P07 inspects the symbol-local hunt fact belonging to the stored protected symbol. It does not compare SPX price with NDX price.

Retirement occurs when the stored protected symbol’s own `is_hunted` becomes true after activation. Retirement evidence stores observation ID, event time, availability time, pair state, and reason code.

No data, unavailable observation, or stale observation is not a breach and is not proof of survival.
