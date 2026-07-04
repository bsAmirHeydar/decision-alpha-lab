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

int FP_HookP07CleanObjects(const FP_HookPhase07Config &cfg,
                           const FP_HookPhase01Config &p01,
                           const FP_HookPhase02Config &p02,
                           const FP_HookPhase03Config &p03,
                           const FP_HookPhase04Config &p04,
                           const FP_HookPhase05Config &p05,
                           const FP_HookPhase06Config &p06)
{
   if(!cfg.clean_before_apply)
      return 0;

   int deleted = 0;
   if(cfg.clean_p01_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p01.object_prefix);
   if(cfg.clean_p02_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p02.object_prefix);
   if(cfg.clean_p03_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p03.object_prefix);
   if(cfg.clean_p04_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p04.object_prefix);
   if(cfg.clean_p05_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p05.object_prefix);
   if(cfg.clean_p06_objects) deleted += FP_HookP07DeleteObjectsByPrefix(p06.object_prefix);
   if(cfg.clean_p07_objects) deleted += FP_HookP07DeleteObjectsByPrefix(cfg.object_prefix);
   return deleted;
}

#endif // __FP_HOOK_PHASE07_VISUAL_MQH__
