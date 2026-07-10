#ifndef __FP_NDS_STRUCTURE_SNAPSHOT_MQH__
#define __FP_NDS_STRUCTURE_SNAPSHOT_MQH__
#property strict

#include "FP_HookPhase02Types.mqh"

#define FP_NDS_STRUCTURE_SNAPSHOT_VERSION "NDS-STRUCTURE-SNAPSHOT-01"

// Read-only handoff cache between Hook Phase 02 and the NDS entry-transition
// layer.  It avoids rebuilding Hook sequences merely to create setup records.
// The cache has no broker authority and never mutates Hook objects.
FP_HookPhase02Sequence g_fp_nds_structure_sequences[];
string g_fp_nds_structure_symbol = "";
ENUM_TIMEFRAMES g_fp_nds_structure_period = PERIOD_CURRENT;
datetime g_fp_nds_structure_captured_at = 0;
bool g_fp_nds_structure_snapshot_ready = false;

void FP_NDSClearStructureSnapshot()
{
   ArrayResize(g_fp_nds_structure_sequences, 0);
   g_fp_nds_structure_symbol = "";
   g_fp_nds_structure_period = PERIOD_CURRENT;
   g_fp_nds_structure_captured_at = 0;
   g_fp_nds_structure_snapshot_ready = false;
}

void FP_NDSCaptureStructureSnapshot(const string symbol,
                                    const ENUM_TIMEFRAMES period,
                                    const FP_HookPhase02Sequence &sequences[])
{
   int count = ArraySize(sequences);
   ArrayResize(g_fp_nds_structure_sequences, count);
   for(int i=0; i<count; i++)
      g_fp_nds_structure_sequences[i] = sequences[i];

   g_fp_nds_structure_symbol = symbol;
   g_fp_nds_structure_period = period;
   g_fp_nds_structure_captured_at = TimeCurrent();
   g_fp_nds_structure_snapshot_ready = true;
}

int FP_NDSCopyStructureSnapshot(FP_HookPhase02Sequence &target[])
{
   int count = ArraySize(g_fp_nds_structure_sequences);
   ArrayResize(target, count);
   for(int i=0; i<count; i++)
      target[i] = g_fp_nds_structure_sequences[i];
   return count;
}

bool FP_NDSStructureSnapshotMatches(const string symbol,
                                    const ENUM_TIMEFRAMES period)
{
   if(!g_fp_nds_structure_snapshot_ready)
      return false;
   if(g_fp_nds_structure_symbol != symbol)
      return false;
   if(g_fp_nds_structure_period != period)
      return false;
   return true;
}

#endif // __FP_NDS_STRUCTURE_SNAPSHOT_MQH__
