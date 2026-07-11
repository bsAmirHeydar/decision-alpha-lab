#ifndef __SF10_RESEARCH_TELEMETRY_MQH__
#define __SF10_RESEARCH_TELEMETRY_MQH__
struct SF10_ResearchTelemetry
{
   long outcomes_observed;
   long outcomes_rejected;
   long frames_sent;
   long frame_failures;
   long frames_received;
   long passes_selected;
   long manifest_failures;
   long export_failures;
   long differential_mismatches;
   long last_finalize_microseconds;
   long maximum_finalize_microseconds;
};
#endif
