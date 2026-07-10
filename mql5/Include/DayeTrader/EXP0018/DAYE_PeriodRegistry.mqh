#ifndef __EXP0018_DAYE_PERIOD_REGISTRY_MQH__
#define __EXP0018_DAYE_PERIOD_REGISTRY_MQH__

#include <DayeTrader/EXP0018/DAYE_Types.mqh>

void DAYE_AppendPeriod(DAYE_PeriodDefinition &items[],const DAYE_PeriodId id,const DAYE_PeriodFamily family,const string code,const int start_second,const int end_second,const int nominal_duration_minutes,const bool wraps_midnight,const bool implementation_ready,const string blocker="")
{
   int index = ArraySize(items);
   ArrayResize(items,index + 1);
   items[index].id = id;
   items[index].family = family;
   items[index].code = code;
   items[index].start_second = start_second;
   items[index].end_second = end_second;
   items[index].nominal_duration_minutes = nominal_duration_minutes;
   items[index].wraps_midnight = wraps_midnight;
   items[index].implementation_ready = implementation_ready;
   items[index].blocker = blocker;
}

int DAYE_BuildCanonicalPeriodRegistry(DAYE_PeriodDefinition &items[])
{
   ArrayResize(items,0);
   DAYE_AppendPeriod(items,DAYE_PERIOD_W,DAYE_FAMILY_WEEKLY,"W",-1,-1,-1,true,false,"ADR-DY-A03 weekly boundary not accepted");
   DAYE_AppendPeriod(items,DAYE_PERIOD_D,DAYE_FAMILY_DAILY,"D",18*3600,17*3600,1380,true,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_GAP,DAYE_FAMILY_GAP,"GAP",17*3600,18*3600,60,false,true);

   DAYE_AppendPeriod(items,DAYE_PERIOD_A,DAYE_FAMILY_SESSION,"A",18*3600,24*3600,360,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_L,DAYE_FAMILY_SESSION,"L",0,6*3600,360,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_N,DAYE_FAMILY_SESSION,"N",6*3600,12*3600,360,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_P,DAYE_FAMILY_SESSION,"P",12*3600,17*3600,300,false,true);

   DAYE_AppendPeriod(items,DAYE_PERIOD_A1,DAYE_FAMILY_SUBCYCLE_90M,"a1",18*3600,19*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_A2,DAYE_FAMILY_SUBCYCLE_90M,"a2",19*3600+30*60,21*3600,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_A3,DAYE_FAMILY_SUBCYCLE_90M,"a3",21*3600,22*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_A4,DAYE_FAMILY_SUBCYCLE_90M,"a4",22*3600+30*60,24*3600,90,false,true);

   DAYE_AppendPeriod(items,DAYE_PERIOD_L1,DAYE_FAMILY_SUBCYCLE_90M,"l1",0,1*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_L2,DAYE_FAMILY_SUBCYCLE_90M,"l2",1*3600+30*60,3*3600,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_L3,DAYE_FAMILY_SUBCYCLE_90M,"l3",3*3600,4*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_L4,DAYE_FAMILY_SUBCYCLE_90M,"l4",4*3600+30*60,6*3600,90,false,true);

   DAYE_AppendPeriod(items,DAYE_PERIOD_N1,DAYE_FAMILY_SUBCYCLE_90M,"n1",6*3600,7*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_N2,DAYE_FAMILY_SUBCYCLE_90M,"n2",7*3600+30*60,9*3600,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_N3,DAYE_FAMILY_SUBCYCLE_90M,"n3",9*3600,10*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_N4,DAYE_FAMILY_SUBCYCLE_90M,"n4",10*3600+30*60,12*3600,90,false,true);

   DAYE_AppendPeriod(items,DAYE_PERIOD_P1,DAYE_FAMILY_SUBCYCLE_90M,"p1",12*3600,13*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_P2,DAYE_FAMILY_SUBCYCLE_90M,"p2",13*3600+30*60,15*3600,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_P3,DAYE_FAMILY_SUBCYCLE_90M,"p3",15*3600,16*3600+30*60,90,false,true);
   DAYE_AppendPeriod(items,DAYE_PERIOD_P4,DAYE_FAMILY_SUBCYCLE_TAIL,"p4",16*3600+30*60,17*3600,30,false,true,"Explicit 30-minute tail");
   return ArraySize(items);
}

bool DAYE_FindPeriodDefinition(const DAYE_PeriodDefinition &items[],const DAYE_PeriodId id,DAYE_PeriodDefinition &definition)
{
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].id == id)
      {
         definition = items[i];
         return true;
      }
   }
   ZeroMemory(definition);
   return false;
}

#endif
