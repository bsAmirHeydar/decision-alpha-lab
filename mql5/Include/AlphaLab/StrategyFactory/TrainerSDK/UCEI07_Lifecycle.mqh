#ifndef ALPHALAB_UCEI07_LIFECYCLE_MQH
#define ALPHALAB_UCEI07_LIFECYCLE_MQH
#include "UCEI07_Enums.mqh"
class CUCEI07TrainerLifecycle{
private:int m_state;
public:
 CUCEI07TrainerLifecycle(){m_state=UCEI07_PHASE_CREATED;}
 int State()const{return m_state;}
 bool Transition(const int next,string &reason){reason="";if(m_state==UCEI07_PHASE_DISPOSED){reason="already_disposed";return false;}bool ok=false;
  if(m_state==UCEI07_PHASE_CREATED&&next==UCEI07_PHASE_CONFIGURED)ok=true;
  else if(m_state==UCEI07_PHASE_CONFIGURED&&next==UCEI07_PHASE_VALIDATED)ok=true;
  else if(m_state==UCEI07_PHASE_VALIDATED&&next==UCEI07_PHASE_FITTING)ok=true;
  else if(m_state==UCEI07_PHASE_FITTING&&next==UCEI07_PHASE_FITTED)ok=true;
  else if(m_state==UCEI07_PHASE_FITTED&&(next==UCEI07_PHASE_CALIBRATED||next==UCEI07_PHASE_PREDICTING||next==UCEI07_PHASE_SERIALIZED))ok=true;
  else if(m_state==UCEI07_PHASE_CALIBRATED&&(next==UCEI07_PHASE_PREDICTING||next==UCEI07_PHASE_SERIALIZED))ok=true;
  else if(m_state==UCEI07_PHASE_PREDICTING&&(next==UCEI07_PHASE_PREDICTING||next==UCEI07_PHASE_SERIALIZED))ok=true;
  else if(next==UCEI07_PHASE_FAILED||next==UCEI07_PHASE_DISPOSED)ok=true;
  if(!ok){reason="illegal_lifecycle_transition";return false;}m_state=next;return true;}
};
#endif
