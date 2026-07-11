#ifndef __SF09_OUTCOME_TELEMETRY_MQH__
#define __SF09_OUTCOME_TELEMETRY_MQH__
struct SF09_OutcomeTelemetry
{
   long registered;
   long observations;
   long duplicate_observations;
   long out_of_order_rejections;
   long fills;
   long no_fills;
   long targets;
   long stops;
   long time_exits;
   long expirations;
   long ambiguities;
   long partial_exits;
   long terminal_outcomes;
   long cost_failures;
   long path_overflows;
};
void SF09_ResetTelemetry(SF09_OutcomeTelemetry &t)
{
   t.registered=0;t.observations=0;t.duplicate_observations=0;t.out_of_order_rejections=0;t.fills=0;t.no_fills=0;
   t.targets=0;t.stops=0;t.time_exits=0;t.expirations=0;t.ambiguities=0;t.partial_exits=0;t.terminal_outcomes=0;
   t.cost_failures=0;t.path_overflows=0;
}
#endif
