# Known-Time Causality

Legacy candidate structures do not carry the exact first tick of detection. Phase 20 therefore does not backdate the event to the cycle start. The adapter assigns `event_time = known_time = confirmation_time = observation UTC time`. Here “confirmation” means confirmation that the raw anatomy observation exists, not trading confirmation.
