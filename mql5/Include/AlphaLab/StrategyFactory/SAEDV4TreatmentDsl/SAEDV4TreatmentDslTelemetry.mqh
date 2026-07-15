#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_TELEMETRY_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_TELEMETRY_MQH

struct SAEDV4DslTelemetrySnapshot
  {
   int program_count;
   int component_count;
   int constraint_count;
   int bound_descriptor_count;
   bool skip_present;
   bool abstain_present;
   int authority_violation_count;
  };

bool SAEDV4DslTelemetrySafe(const SAEDV4DslTelemetrySnapshot &value)
  {
   return(value.program_count>=2 && value.component_count>=2 && value.constraint_count>=0 && value.bound_descriptor_count>=0 && value.skip_present && value.abstain_present && value.authority_violation_count==0);
  }
#endif
