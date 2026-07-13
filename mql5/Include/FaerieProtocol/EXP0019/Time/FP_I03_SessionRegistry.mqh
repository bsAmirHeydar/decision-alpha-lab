#ifndef __EXP0019_FP_I03_SESSION_REGISTRY_MQH__
#define __EXP0019_FP_I03_SESSION_REGISTRY_MQH__

#include <FaerieProtocol/EXP0019/Core/FP_I02_Hash.mqh>
#include "FP_I03_Types.mqh"

#define FP_I03_A_START 64800
#define FP_I03_A_END 14400
#define FP_I03_L_START 14400
#define FP_I03_L_END 34200
#define FP_I03_N_START 34200
#define FP_I03_N_END 61200
#define FP_I03_GAP_START 61200
#define FP_I03_GAP_END 64800

void FP_I03_BuildSessionDefinition(const FP_I03_CalendarSegment code,FP_I03_SessionDefinition &d)
  {
   ZeroMemory(d);d.code=code;
   if(code==FP_I03_SEGMENT_A){d.start_second=FP_I03_A_START;d.end_second=FP_I03_A_END;d.wraps_midnight=true;d.ordinal=0;}
   else if(code==FP_I03_SEGMENT_L){d.start_second=FP_I03_L_START;d.end_second=FP_I03_L_END;d.wraps_midnight=false;d.ordinal=1;}
   else if(code==FP_I03_SEGMENT_N){d.start_second=FP_I03_N_START;d.end_second=FP_I03_N_END;d.wraps_midnight=false;d.ordinal=2;}
   d.definition_id=FP_I02_CompactId("FPSESSDEF",FP_I03_SegmentToString(code)+"|"+IntegerToString(d.start_second)+"|"+IntegerToString(d.end_second)+"|"+IntegerToString(d.ordinal));
  }

FP_I03_CalendarSegment FP_I03_ClassifyIntraday(const int second_of_day)
  {
   if(second_of_day>=FP_I03_A_START || second_of_day<FP_I03_A_END)return FP_I03_SEGMENT_A;
   if(second_of_day>=FP_I03_L_START && second_of_day<FP_I03_L_END)return FP_I03_SEGMENT_L;
   if(second_of_day>=FP_I03_N_START && second_of_day<FP_I03_N_END)return FP_I03_SEGMENT_N;
   return FP_I03_SEGMENT_DAILY_GAP;
  }

#endif
