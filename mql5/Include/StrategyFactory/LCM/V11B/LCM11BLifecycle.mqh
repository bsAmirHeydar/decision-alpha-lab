#ifndef __LCM11B_LIFECYCLE_MQH__
#define __LCM11B_LIFECYCLE_MQH__
enum ENUM_LCM11B_LIFECYCLE{LCM11B_INITIALIZE=0,LCM11B_HISTORICAL_BACKFILL=1,LCM11B_INCREMENTAL_UPDATE=2,LCM11B_RESTART_RECONCILE=3,LCM11B_CHART_CHANGE_RECONCILE=4,LCM11B_OWNED_CLEANUP=5};
class CLCM11BLifecycleState
  {
private:ENUM_LCM11B_LIFECYCLE m_state;long m_revision;
public:CLCM11BLifecycleState(){m_state=LCM11B_INITIALIZE;m_revision=0;}void Transition(const ENUM_LCM11B_LIFECYCLE state){m_state=state;m_revision++;}ENUM_LCM11B_LIFECYCLE State()const{return m_state;}long Revision()const{return m_revision;}
  };
#endif
