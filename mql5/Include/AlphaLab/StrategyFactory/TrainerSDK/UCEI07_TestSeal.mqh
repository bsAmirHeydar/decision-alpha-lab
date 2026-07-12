#ifndef ALPHALAB_UCEI07_TEST_SEAL_MQH
#define ALPHALAB_UCEI07_TEST_SEAL_MQH
#include "UCEI07_Contracts.mqh"
class CUCEI07TestSeal{
private:bool m_selection_locked;long m_sequence;long m_test_reads;
public:
 CUCEI07TestSeal(){m_selection_locked=false;m_sequence=0;m_test_reads=0;}
 void LockSelection(){m_selection_locked=true;}
 bool SelectionLocked()const{return m_selection_locked;}
 bool Authorize(const int role,const int purpose,const string phase,const string trainer_key,UCEI07_AccessAuditRecord &audit) {
  m_sequence++;audit.sequence=m_sequence;audit.role=role;audit.purpose=purpose;audit.phase=phase;audit.trainer_key=trainer_key;audit.allowed=false;audit.reason="";
  bool role_ok=false;
  if(purpose==UCEI07_ACCESS_FIT)role_ok=(role==UCEI07_ROLE_TRAIN||role==UCEI07_ROLE_FINAL_TRAIN);
  else if(purpose==UCEI07_ACCESS_CALIBRATE)role_ok=(role==UCEI07_ROLE_CALIBRATION||role==UCEI07_ROLE_FINAL_CALIBRATION);
  else if(purpose==UCEI07_ACCESS_SELECT_THRESHOLD)role_ok=(role==UCEI07_ROLE_THRESHOLD||role==UCEI07_ROLE_FINAL_THRESHOLD);
  else if(purpose==UCEI07_ACCESS_PREDICT_OOF)role_ok=(role==UCEI07_ROLE_OOF_HOLDOUT);
  else if(purpose==UCEI07_ACCESS_PREDICT_FINAL_TEST)role_ok=(role==UCEI07_ROLE_FINAL_TEST&&m_selection_locked);
  else if(purpose==UCEI07_ACCESS_EXPLAIN||purpose==UCEI07_ACCESS_PACKAGE)role_ok=(role!=UCEI07_ROLE_PURGED&&role!=UCEI07_ROLE_EMBARGO);
  if(role==UCEI07_ROLE_FINAL_TEST&&!m_selection_locked){audit.reason="final_test_sealed_until_selection_lock";return false;}if(role==UCEI07_ROLE_FINAL_TEST&&m_test_reads>0){audit.reason="final_test_one_shot_already_consumed";return false;}
  if(!role_ok){audit.reason="role_purpose_mismatch";return false;}audit.allowed=true;audit.reason="authorized";if(role==UCEI07_ROLE_FINAL_TEST)m_test_reads++;return true;
 }
};
#endif
