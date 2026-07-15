#ifndef ALPHALAB_OPERATIONS_INCIDENT_GATE_MQH
#define ALPHALAB_OPERATIONS_INCIDENT_GATE_MQH
enum ALOperationsIncidentSeverity { AL_OPS_INCIDENT_INFO=0, AL_OPS_INCIDENT_WARNING=1, AL_OPS_INCIDENT_HIGH=2, AL_OPS_INCIDENT_CRITICAL=3 };
enum ALOperationsIncidentState { AL_OPS_INCIDENT_OPEN=0, AL_OPS_INCIDENT_CONTAINED=1, AL_OPS_INCIDENT_RESOLVED=2, AL_OPS_INCIDENT_CLOSED=3 };
struct ALOperationsIncidentGate { ALOperationsIncidentSeverity severity; ALOperationsIncidentState state; };
bool ALOpsIncidentAllowsOperation(const ALOperationsIncidentGate &incident){ return incident.state==AL_OPS_INCIDENT_CLOSED || incident.severity<AL_OPS_INCIDENT_HIGH; }
#endif
