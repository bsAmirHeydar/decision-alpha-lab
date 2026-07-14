#ifndef __FP_I12_DIAGNOSTICS_MQH__
#define __FP_I12_DIAGNOSTICS_MQH__
#include "FP_I12_Contracts.mqh"
#include "FP_I12_Hash.mqh"
SFP_I12_Diagnostic FP_I12_BuildDiagnostic(const bool ready,const long panel_updates,const long delivered,const long suppressed,const long exported,const string reason){SFP_I12_Diagnostic d;d.ready=ready;d.panel_updates=panel_updates;d.alert_deliveries=delivered;d.alert_suppressed=suppressed;d.export_records=exported;d.reason_code=reason;d.diagnostic_hash=FP_I12_Hash(IntegerToString((int)ready)+"|"+IntegerToString((int)panel_updates)+"|"+IntegerToString((int)delivered)+"|"+IntegerToString((int)suppressed)+"|"+IntegerToString((int)exported)+"|"+reason);return d;}
#endif
