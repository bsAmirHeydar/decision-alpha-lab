#ifndef __SF17_EXECUTION_TELEMETRY_MQH__
#define __SF17_EXECUTION_TELEMETRY_MQH__
struct SF17_ExecutionTelemetry{long intents_received;long intents_accepted;long intents_rejected;long orders_working;long orders_filled;long orders_expired;long orders_canceled;long fills;long positions_open;long positions_closed;long duplicate_intents;long stale_quotes;};
void SF17_ResetTelemetry(SF17_ExecutionTelemetry &t){ZeroMemory(t);}
#endif
