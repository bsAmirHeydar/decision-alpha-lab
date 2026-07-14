#ifndef __FP_I12_ACTION_ROUTER_MQH__
#define __FP_I12_ACTION_ROUTER_MQH__
#include "FP_I12_Enums.mqh"
class FP_I12_ActionRouter {private:bool m_rebuild_requested;public:FP_I12_ActionRouter(){m_rebuild_requested=false;}void Record(const ENUM_FP_I12_ACTION action){if(action==FP_I12_ACTION_REBUILD_REQUEST)m_rebuild_requested=true;}bool RebuildRequested()const{return m_rebuild_requested;}};
#endif
