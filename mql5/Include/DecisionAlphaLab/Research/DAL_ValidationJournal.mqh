#ifndef __DAL_VALIDATION_JOURNAL_MQH__
#define __DAL_VALIDATION_JOURNAL_MQH__

#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

void DAL_EnsureDefaultJournalFolders()
{
   FolderCreate("DecisionAlphaLab");
   FolderCreate("DecisionAlphaLab\\M0001");
}

int DAL_OpenJournalWrite(const string file_name)
{
   DAL_EnsureDefaultJournalFolders();
   return FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_ANSI, ',');
}

void DAL_WriteM0001NodeJournal(
   const string file_name,
   const DALLRuleNode &nodes[],
   const int nodes_count
)
{
   int h = DAL_OpenJournalWrite(file_name);
   if(h == INVALID_HANDLE)
      return;

   FileWrite(h, "id", "type", "node_time", "active_from_time", "index", "active_index", "price");
   for(int i = 0; i < nodes_count; i++)
   {
      FileWrite(
         h,
         nodes[i].id,
         DAL_NodeTypeToString(nodes[i].type),
         TimeToString(nodes[i].time, TIME_DATE | TIME_MINUTES),
         TimeToString(nodes[i].active_from_time, TIME_DATE | TIME_MINUTES),
         nodes[i].index,
         nodes[i].active_from_index,
         DoubleToString(nodes[i].price, _Digits)
      );
   }

   FileClose(h);
}

void DAL_WriteM0001EventJournal(
   const string file_name,
   const DALM0001Event &events[],
   const int events_count
)
{
   int h = DAL_OpenJournalWrite(file_name);
   if(h == INVALID_HANDLE)
      return;

   FileWrite(h, "id", "node_id", "type", "entry_time", "exit_time", "rtv", "hunted", "mean_before", "mean_inside");
   for(int i = 0; i < events_count; i++)
   {
      FileWrite(
         h,
         events[i].id,
         events[i].node_id,
         DAL_NodeTypeToString(events[i].node_type),
         TimeToString(events[i].entry_time, TIME_DATE | TIME_MINUTES),
         TimeToString(events[i].exit_time, TIME_DATE | TIME_MINUTES),
         DoubleToString(events[i].rtv, 6),
         DAL_BoolToString(events[i].hunted),
         DoubleToString(events[i].mean_before, 6),
         DoubleToString(events[i].mean_inside, 6)
      );
   }

   FileClose(h);
}

#endif
