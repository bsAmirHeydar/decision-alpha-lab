#ifndef __SF11_STATISTICS_TELEMETRY_MQH__
#define __SF11_STATISTICS_TELEMETRY_MQH__
struct SF11_StatisticsTelemetry
{
   long samples_observed;long samples_rejected;long groups_created;long summaries_emitted;long intervals_emitted;long null_assignments;long null_unmatched;long export_failures;long lineage_failures;long last_finalize_microseconds;long maximum_finalize_microseconds;
};
#endif
