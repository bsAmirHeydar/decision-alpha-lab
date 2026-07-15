#ifndef ALPHALAB_OPERATIONS_EOD_GUARD_MQH
#define ALPHALAB_OPERATIONS_EOD_GUARD_MQH
struct ALOperationsEodEvidence { bool all_events_persisted; bool all_intents_terminal; bool exact_reconciliation; int unresolved_high_incidents; int unresolved_critical_incidents; double daily_loss_units; };
bool ALOpsEodPasses(const ALOperationsEodEvidence &e,const double max_daily_loss){ return e.all_events_persisted&&e.all_intents_terminal&&e.exact_reconciliation&&e.unresolved_high_incidents==0&&e.unresolved_critical_incidents==0&&e.daily_loss_units<=max_daily_loss; }
#endif
