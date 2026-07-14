#ifndef __FP_I14_TRACE_EXPORTER_MQH__
#define __FP_I14_TRACE_EXPORTER_MQH__
#include "FP_I14_TraceLedger.mqh"
bool FP_I14_ExportLedger(const CFP_I14_TraceLedger &ledger,const string file_name,string &reason){int h=FileOpen(file_name,FILE_WRITE|FILE_READ|FILE_CSV|FILE_COMMON|FILE_ANSI);if(h==INVALID_HANDLE){reason="FP_DIAG_EXPORT_OPEN_FAILED";return false;}FileSeek(h,0,SEEK_END);for(int i=0;i<ledger.Count();i++){FP_I14_TraceEvent e;ledger.Get(i,e);FileWrite(h,e.product,e.sequence,e.event_time,e.event_type,e.semantic_id,e.payload_hash,e.config_hash,e.source_revision_id,e.state,e.buffer_index,DoubleToString(e.numeric_value,10));}FileClose(h);reason="FP_DIAG_EXPORT_APPENDED";return true;}
#endif
