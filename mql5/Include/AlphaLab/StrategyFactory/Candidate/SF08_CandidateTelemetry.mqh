#ifndef __SF08_CANDIDATE_TELEMETRY_MQH__
#define __SF08_CANDIDATE_TELEMETRY_MQH__
struct SF08_CandidateTelemetry
{
   long build_requests;
   long templates_considered;
   long templates_disabled;
   long policy_skips;
   long policy_errors;
   long geometry_rejections;
   long duplicates_rejected;
   long candidates_emitted;
   long queue_overflows;
   long total_build_microseconds;
   long maximum_build_microseconds;
};
void SF08_ResetCandidateTelemetry(SF08_CandidateTelemetry &t)
{t.build_requests=0;t.templates_considered=0;t.templates_disabled=0;t.policy_skips=0;t.policy_errors=0;t.geometry_rejections=0;t.duplicates_rejected=0;t.candidates_emitted=0;t.queue_overflows=0;t.total_build_microseconds=0;t.maximum_build_microseconds=0;}
#endif
