#ifndef __EXP0018_DAYE_CONFIRMATION_STORE_MQH__
#define __EXP0018_DAYE_CONFIRMATION_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationStateMachine.mqh>

class CDayeConfirmationStore
{
private:
   DAYE_ConfirmationCandidate m_candidates[];
   DAYE_ConfirmationResult m_results[];
   string m_finalized_observation_ids[];
   DAYE_ConfirmationSourceMemory m_source_memory[];

   void RemoveCandidateAt(const int index)
   {
      int count=ArraySize(m_candidates);
      if(index < 0 || index >= count) return;
      for(int i=index;i<count-1;i++) m_candidates[i]=m_candidates[i+1];
      ArrayResize(m_candidates,count-1);
   }

public:
   CDayeConfirmationStore(void)
   {
      ArrayResize(m_candidates,0);
      ArrayResize(m_results,0);
      ArrayResize(m_finalized_observation_ids,0);
      ArrayResize(m_source_memory,0);
   }

   void Clear(void)
   {
      ArrayResize(m_candidates,0);
      ArrayResize(m_results,0);
      ArrayResize(m_finalized_observation_ids,0);
      ArrayResize(m_source_memory,0);
   }

   int CandidateCount(void) { return ArraySize(m_candidates); }
   int ResultCount(void) { return ArraySize(m_results); }
   int FinalizedIdCount(void) { return ArraySize(m_finalized_observation_ids); }
   int SourceMemoryCount(void) { return ArraySize(m_source_memory); }

   bool GetCandidate(const int index,DAYE_ConfirmationCandidate &candidate)
   {
      if(index < 0 || index >= ArraySize(m_candidates)) return false;
      candidate=m_candidates[index];
      return true;
   }

   bool SetCandidate(const int index,const DAYE_ConfirmationCandidate &candidate)
   {
      if(index < 0 || index >= ArraySize(m_candidates)) return false;
      m_candidates[index]=candidate;
      return true;
   }

   int FindCandidateIndexByObservationId(const string observation_id)
   {
      for(int i=0;i<ArraySize(m_candidates);i++)
         if(m_candidates[i].observation_id == observation_id) return i;
      return -1;
   }

   bool AppendCandidate(const DAYE_ConfirmationCandidate &candidate,const int maximum_count)
   {
      if(candidate.candidate_id == "" || FindCandidateIndexByObservationId(candidate.observation_id) >= 0)
         return false;
      if(ArraySize(m_candidates) >= maximum_count)
         return false;
      int index=ArraySize(m_candidates);
      ArrayResize(m_candidates,index+1);
      m_candidates[index]=candidate;
      return true;
   }

   bool RemoveCandidateByObservationId(const string observation_id)
   {
      int index=FindCandidateIndexByObservationId(observation_id);
      if(index < 0) return false;
      RemoveCandidateAt(index);
      return true;
   }

   bool IsObservationFinalized(const string observation_id)
   {
      for(int i=0;i<ArraySize(m_finalized_observation_ids);i++)
         if(m_finalized_observation_ids[i] == observation_id) return true;
      return false;
   }

   bool RememberFinalizedObservation(const string observation_id,const int maximum_count)
   {
      if(observation_id == "") return false;
      if(IsObservationFinalized(observation_id)) return true;
      int count=ArraySize(m_finalized_observation_ids);
      if(count >= maximum_count)
      {
         for(int i=1;i<count;i++) m_finalized_observation_ids[i-1]=m_finalized_observation_ids[i];
         ArrayResize(m_finalized_observation_ids,count-1);
         count--;
      }
      ArrayResize(m_finalized_observation_ids,count+1);
      m_finalized_observation_ids[count]=observation_id;
      return true;
   }

   bool AppendResult(const DAYE_ConfirmationResult &result,const int maximum_count)
   {
      for(int i=0;i<ArraySize(m_results);i++)
         if(m_results[i].result_id == result.result_id) return false;
      int count=ArraySize(m_results);
      if(count >= maximum_count)
      {
         for(int i=1;i<count;i++) m_results[i-1]=m_results[i];
         ArrayResize(m_results,count-1);
         count--;
      }
      ArrayResize(m_results,count+1);
      m_results[count]=result;
      return true;
   }

   bool GetResult(const int index,DAYE_ConfirmationResult &result)
   {
      if(index < 0 || index >= ArraySize(m_results)) return false;
      result=m_results[index];
      return true;
   }

   int ExportCandidates(DAYE_ConfirmationCandidate &items[])
   {
      ArrayResize(items,ArraySize(m_candidates));
      for(int i=0;i<ArraySize(m_candidates);i++) items[i]=m_candidates[i];
      return ArraySize(items);
   }

   int ExportResults(DAYE_ConfirmationResult &items[])
   {
      ArrayResize(items,ArraySize(m_results));
      for(int i=0;i<ArraySize(m_results);i++) items[i]=m_results[i];
      return ArraySize(items);
   }

   int ExportFinalizedIds(string &items[])
   {
      ArrayResize(items,ArraySize(m_finalized_observation_ids));
      for(int i=0;i<ArraySize(m_finalized_observation_ids);i++) items[i]=m_finalized_observation_ids[i];
      return ArraySize(items);
   }

   bool FindSourceMemory(const string observation_id,DAYE_ConfirmationSourceMemory &memory)
   {
      for(int i=0;i<ArraySize(m_source_memory);i++)
      {
         if(m_source_memory[i].observation_id == observation_id)
         {
            memory=m_source_memory[i];
            return true;
         }
      }
      return false;
   }

   void ReplaceSourceMemory(const DAYE_HuntObservation &observations[])
   {
      ArrayResize(m_source_memory,ArraySize(observations));
      for(int i=0;i<ArraySize(observations);i++)
      {
         m_source_memory[i].observation_id=observations[i].observation_id;
         m_source_memory[i].status=observations[i].status;
         m_source_memory[i].pair_state=observations[i].pair_state;
         m_source_memory[i].availability_time_utc=observations[i].availability_time_utc;
         m_source_memory[i].is_one_sided=observations[i].is_one_sided;
      }
   }
};

bool DAYE_FindHuntObservationById(const DAYE_HuntObservation &items[],const string observation_id,DAYE_HuntObservation &observation)
{
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].observation_id == observation_id)
      {
         observation=items[i];
         return true;
      }
   }
   return false;
}

#endif
