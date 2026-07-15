#ifndef ALPHALAB_QUALIFICATION_TELEMETRY_MQH
#define ALPHALAB_QUALIFICATION_TELEMETRY_MQH
struct ALQualificationTelemetry { long evaluated_at_ms; int passed_gates; int failed_gates; int pending_gates; bool kill_switch_engaged; bool activation_allowed; string qualification_hash; };
bool ALQualificationTelemetryConsistent(const ALQualificationTelemetry &telemetry){ return telemetry.evaluated_at_ms>=0 && telemetry.passed_gates>=0 && telemetry.failed_gates>=0 && telemetry.pending_gates>=0 && (!telemetry.activation_allowed || (telemetry.failed_gates==0 && telemetry.pending_gates==0 && !telemetry.kill_switch_engaged)); }
#endif
