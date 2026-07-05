#ifndef __FP_HOOK_PHASE07_VISUAL_MQH__
#define __FP_HOOK_PHASE07_VISUAL_MQH__
#property strict

#include "FP_HookPhase07Rules.mqh"

int FP_HookP07DeleteObjectsByPrefix(const string prefix)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int deleted = 0;
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
      {
         if(ObjectDelete(0, name))
            deleted++;
      }
   }
   return deleted;
}

int FP_HookP07DeleteObjectsByPrefixes(const string &prefixes[])
{
   int prefix_count = ArraySize(prefixes);
   if(prefix_count <= 0)
      return 0;

   int deleted = 0;
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      bool should_delete = false;

      for(int p=0; p<prefix_count && !should_delete; p++)
      {
         string prefix = prefixes[p];
         if(StringLen(prefix) <= 0)
            continue;

         bool duplicate = false;
         for(int q=0; q<p; q++)
         {
            if(prefixes[q] == prefix)
            {
               duplicate = true;
               break;
            }
         }
         if(duplicate)
            continue;

         if(StringFind(name, prefix) == 0)
            should_delete = true;
      }

      if(should_delete && ObjectDelete(0, name))
         deleted++;
   }
   return deleted;
}

int FP_HookP07CleanObjects(const FP_HookPhase07Config &cfg,
                           const FP_HookPhase01Config &p01,
                           const FP_HookPhase02Config &p02,
                           const FP_HookPhase03Config &p03,
                           const FP_HookPhase04Config &p04,
                           const FP_HookPhase05Config &p05,
                           const FP_HookPhase06Config &p06)
{
   const bool sequence_debug_lens = (cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG);
   if(!cfg.clean_before_apply && !sequence_debug_lens)
      return 0;

   string prefixes[];
   ArrayResize(prefixes, 0);

   if(cfg.clean_common_hook_prefix || sequence_debug_lens)
   {
      int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = cfg.common_hook_object_prefix;
   }
   if(cfg.clean_p01_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p01.object_prefix; }
   if(cfg.clean_p02_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p02.object_prefix; }
   if(cfg.clean_p03_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p03.object_prefix; }
   if(cfg.clean_p04_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p04.object_prefix; }
   if(cfg.clean_p05_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p05.object_prefix; }
   if(cfg.clean_p06_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = p06.object_prefix; }
   if(cfg.clean_p07_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = cfg.object_prefix; }
   if(cfg.clean_p08_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = cfg.clean_p08_object_prefix; }
   if(cfg.clean_p09_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = cfg.clean_p09_object_prefix; }
   if(cfg.clean_p10_objects) { int n = ArraySize(prefixes); ArrayResize(prefixes, n + 1); prefixes[n] = cfg.clean_p10_object_prefix; }

   return FP_HookP07DeleteObjectsByPrefixes(prefixes);
}

#endif // __FP_HOOK_PHASE07_VISUAL_MQH__
