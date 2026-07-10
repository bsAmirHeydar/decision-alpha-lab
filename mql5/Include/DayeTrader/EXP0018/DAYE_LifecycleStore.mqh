#ifndef __EXP0018_DAYE_LIFECYCLE_STORE_MQH__
#define __EXP0018_DAYE_LIFECYCLE_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleIdentity.mqh>

class CDayeLifecycleStore
{
private:
   DAYE_ReferenceLifecycleRecord m_references[];
   DAYE_ReferenceUseRecord m_uses[];
   string m_processed_result_ids[];

public:
   CDayeLifecycleStore(void)
   {
      ArrayResize(m_references,0);
      ArrayResize(m_uses,0);
      ArrayResize(m_processed_result_ids,0);
   }

   void Clear(void)
   {
      ArrayResize(m_references,0);
      ArrayResize(m_uses,0);
      ArrayResize(m_processed_result_ids,0);
   }

   int ReferenceCount(void) { return ArraySize(m_references); }
   int UseCount(void) { return ArraySize(m_uses); }
   int ProcessedResultCount(void) { return ArraySize(m_processed_result_ids); }

   int FindReferenceIndex(const string reference_id)
   {
      for(int i=0;i<ArraySize(m_references);i++)
         if(m_references[i].reference_id == reference_id) return i;
      return -1;
   }

   bool GetReference(const int index,DAYE_ReferenceLifecycleRecord &record)
   {
      if(index<0 || index>=ArraySize(m_references)) return false;
      record=m_references[index];
      return true;
   }

   bool SetReference(const int index,const DAYE_ReferenceLifecycleRecord &record)
   {
      if(index<0 || index>=ArraySize(m_references)) return false;
      m_references[index]=record;
      return true;
   }

   bool AppendReference(const DAYE_ReferenceLifecycleRecord &record,const int maximum_count)
   {
      if(record.reference_id=="" || FindReferenceIndex(record.reference_id)>=0) return false;
      if(ArraySize(m_references)>=maximum_count) return false;
      int n=ArraySize(m_references);
      ArrayResize(m_references,n+1);
      m_references[n]=record;
      return true;
   }

   bool HasExactOpportunityUse(const string key)
   {
      for(int i=0;i<ArraySize(m_uses);i++)
         if(m_uses[i].exact_opportunity_use_key==key && m_uses[i].is_accepted) return true;
      return false;
   }

   bool HasUseId(const string use_id)
   {
      for(int i=0;i<ArraySize(m_uses);i++)
         if(m_uses[i].use_id==use_id) return true;
      return false;
   }

   bool AppendUse(const DAYE_ReferenceUseRecord &use,const int maximum_count)
   {
      if(use.use_id=="" || HasUseId(use.use_id)) return false;
      int n=ArraySize(m_uses);
      if(n>=maximum_count)
      {
         for(int i=1;i<n;i++) m_uses[i-1]=m_uses[i];
         ArrayResize(m_uses,n-1);
         n--;
      }
      ArrayResize(m_uses,n+1);
      m_uses[n]=use;
      return true;
   }

   bool IsResultProcessed(const string result_id)
   {
      for(int i=0;i<ArraySize(m_processed_result_ids);i++)
         if(m_processed_result_ids[i]==result_id) return true;
      return false;
   }

   bool RememberProcessedResult(const string result_id,const int maximum_count)
   {
      if(result_id=="") return false;
      if(IsResultProcessed(result_id)) return true;
      int n=ArraySize(m_processed_result_ids);
      if(n>=maximum_count)
      {
         for(int i=1;i<n;i++) m_processed_result_ids[i-1]=m_processed_result_ids[i];
         ArrayResize(m_processed_result_ids,n-1);
         n--;
      }
      ArrayResize(m_processed_result_ids,n+1);
      m_processed_result_ids[n]=result_id;
      return true;
   }

   int ExportReferences(DAYE_ReferenceLifecycleRecord &items[])
   {
      ArrayResize(items,ArraySize(m_references));
      for(int i=0;i<ArraySize(m_references);i++) items[i]=m_references[i];
      return ArraySize(items);
   }

   int ExportUses(DAYE_ReferenceUseRecord &items[])
   {
      ArrayResize(items,ArraySize(m_uses));
      for(int i=0;i<ArraySize(m_uses);i++) items[i]=m_uses[i];
      return ArraySize(items);
   }

   int ExportProcessedResultIds(string &items[])
   {
      ArrayResize(items,ArraySize(m_processed_result_ids));
      for(int i=0;i<ArraySize(m_processed_result_ids);i++) items[i]=m_processed_result_ids[i];
      return ArraySize(items);
   }
};

#endif
