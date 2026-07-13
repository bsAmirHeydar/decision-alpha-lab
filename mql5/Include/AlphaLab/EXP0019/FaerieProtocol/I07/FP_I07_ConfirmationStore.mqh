#ifndef FP_I07_CONFIRMATION_STORE_MQH
#define FP_I07_CONFIRMATION_STORE_MQH
class CFP_I07_ResultStore
{
private: string m_candidate_ids[]; string m_result_hashes[];
public:
   bool HasCandidate(const string id) const { for(int i=0;i<ArraySize(m_candidate_ids);i++) if(m_candidate_ids[i]==id) return true; return false; }
   bool Add(const string candidate_id,const string result_hash) { if(HasCandidate(candidate_id)) return false; int n=ArraySize(m_candidate_ids); ArrayResize(m_candidate_ids,n+1); ArrayResize(m_result_hashes,n+1); m_candidate_ids[n]=candidate_id; m_result_hashes[n]=result_hash; return true; }
   int Size() const { return ArraySize(m_candidate_ids); }
};
#endif
