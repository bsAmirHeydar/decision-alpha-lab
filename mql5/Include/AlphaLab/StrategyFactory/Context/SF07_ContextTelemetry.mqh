#ifndef __SF07_CONTEXT_TELEMETRY_MQH__
#define __SF07_CONTEXT_TELEMETRY_MQH__

struct SF07_ContextTelemetry
{
   long build_count;
   long build_failures;
   long feature_computations;
   long feature_cache_hits;
   long stale_rejections;
   long missing_rejections;
   long dependency_failures;
   long vector_builds;
   long total_build_microseconds;
   long maximum_build_microseconds;
};

void SF07_ResetContextTelemetry(SF07_ContextTelemetry &telemetry)
{
   telemetry.build_count = 0;
   telemetry.build_failures = 0;
   telemetry.feature_computations = 0;
   telemetry.feature_cache_hits = 0;
   telemetry.stale_rejections = 0;
   telemetry.missing_rejections = 0;
   telemetry.dependency_failures = 0;
   telemetry.vector_builds = 0;
   telemetry.total_build_microseconds = 0;
   telemetry.maximum_build_microseconds = 0;
}

#endif
