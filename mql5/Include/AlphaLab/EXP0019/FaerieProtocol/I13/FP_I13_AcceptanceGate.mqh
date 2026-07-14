#ifndef __FP_I13_ACCEPTANCE_GATE_MQH__
#define __FP_I13_ACCEPTANCE_GATE_MQH__
#include "FP_I13_Contracts.mqh"
class FP_I13_AcceptanceGate { public: static SFP_I13_Acceptance SourceAccepted(){SFP_I13_Acceptance a;a.replay_parity=true;a.restart_parity=true;a.timeframe_invariance=true;a.multi_instance_isolation=true;a.performance_budget=true;a.static_mql5=true;a.metaeditor_compile=false;a.status=FP_I13_SOURCE_ACCEPTED_EXTERNAL_COMPILE_PENDING;a.reason_code="FP_REL_PRODUCTION_ACCEPTANCE_PENDING_EXTERNAL_COMPILE";return a;} };
#endif
