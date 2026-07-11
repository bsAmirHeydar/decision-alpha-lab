#ifndef __SF12_VALIDATION_EXPORTER_MQH__
#define __SF12_VALIDATION_EXPORTER_MQH__
#include "SF12_ValidationEngine.mqh"
class CSF12ValidationExporter
{
public:
   bool WriteFoldCsv(const string filename,const SF12_ValidationFold &folds[],string &error) const
   {
      const int h=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');if(h==INVALID_HANDLE){error="cannot open fold CSV: "+IntegerToString(GetLastError());return false;}
      FileWrite(h,"fold_id","ordinal","plan_hash","train_start","train_end","validation_start","validation_end","test_start","test_end","fold_hash");
      for(int i=0;i<ArraySize(folds);i++){const SF12_ValidationFold f=folds[i];FileWrite(h,f.fold_id,f.ordinal,f.plan_hash,f.train.start_utc_msc,f.train.end_utc_msc,f.validation.start_utc_msc,f.validation.end_utc_msc,f.test.start_utc_msc,f.test.end_utc_msc,f.fold_hash);}FileClose(h);error="";return true;
   }
   bool WriteGateCsv(const string filename,const SF12_PromotionDecision &d,string &error) const
   {
      const int h=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');if(h==INVALID_HANDLE){error="cannot open gate CSV: "+IntegerToString(GetLastError());return false;}
      FileWrite(h,"decision_id","selected_trial_id","promotion_status","gate_id","gate_status","observed","comparison","threshold","reason_code","evidence_hash");
      for(int i=0;i<ArraySize(d.gates);i++){const SF12_GateResult g=d.gates[i];FileWrite(h,d.decision_id,d.selected_trial_id,(int)d.status,g.gate_id,(int)g.status,g.observed_value,g.comparison,g.threshold_value,g.reason_code,g.evidence_hash);}FileClose(h);error="";return true;
   }
};
#endif
