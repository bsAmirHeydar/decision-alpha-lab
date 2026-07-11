#ifndef __SF12_VALIDATION_TELEMETRY_MQH__
#define __SF12_VALIDATION_TELEMETRY_MQH__
struct SF12_ValidationTelemetry
{
   long observations_accepted;long observations_rejected;long ambiguous_excluded;long folds_seen;long gates_evaluated;long gates_failed;
   long last_finalize_microseconds;long maximum_finalize_microseconds;
};
#endif
