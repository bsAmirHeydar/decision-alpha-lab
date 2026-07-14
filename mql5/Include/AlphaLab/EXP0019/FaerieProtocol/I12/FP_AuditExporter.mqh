#ifndef __FP_AUDIT_EXPORTER_MQH__
#define __FP_AUDIT_EXPORTER_MQH__
#include "FP_I12_Contracts.mqh"
#include "FP_I12_Hash.mqh"
class FP_I12_AuditExporter {
 private:SFP_I12_Config m_cfg;long m_records;
 string FileName(const string ext)const{return m_cfg.export_prefix+"_"+FP_I12_Hash(m_cfg.instance_id)+"."+ext;}
 bool AppendLine(const string name,const string line){int h=FileOpen(name,FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI|FILE_COMMON);if(h==INVALID_HANDLE)return false;FileSeek(h,0,SEEK_END);FileWriteString(h,line+"
");FileFlush(h);FileClose(h);return true;}
 public:
 FP_I12_AuditExporter(){m_records=0;}void Initialize(const SFP_I12_Config &cfg){m_cfg=cfg;}
 bool ExportSnapshot(const SFP_I10_EngineSnapshot &s){if(!m_cfg.export_enabled)return false;string csv=TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS)+","+s.instance.instance_id+","+s.snapshot_hash+","+IntegerToString((int)s.health.overall)+","+DoubleToString(s.output.active_ww_direction,0)+","+DoubleToString(s.output.confirmed_signal_count,0)+","+DoubleToString(s.output.suppressed_by_ww_count,0)+","+DoubleToString(s.output.suppressed_by_quota_count,0);string json="{"time":""+TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS)+"","instance_id":""+s.instance.instance_id+"","snapshot_hash":""+s.snapshot_hash+"","health":"+IntegerToString((int)s.health.overall)+","ww":"+DoubleToString(s.output.active_ww_direction,0)+","confirmed":"+DoubleToString(s.output.confirmed_signal_count,0)+"}";bool ok=true;if(m_cfg.export_format==FP_I12_EXPORT_CSV||m_cfg.export_format==FP_I12_EXPORT_BOTH)ok=AppendLine(FileName("csv"),csv)&&ok;if(m_cfg.export_format==FP_I12_EXPORT_JSONL||m_cfg.export_format==FP_I12_EXPORT_BOTH)ok=AppendLine(FileName("jsonl"),json)&&ok;if(ok)m_records++;return ok;}
 long Records()const{return m_records;}
};
#endif
