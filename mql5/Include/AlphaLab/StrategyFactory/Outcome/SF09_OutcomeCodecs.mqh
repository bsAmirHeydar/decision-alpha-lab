#ifndef __SF09_OUTCOME_CODECS_MQH__
#define __SF09_OUTCOME_CODECS_MQH__
#include "SF09_OutcomeRecord.mqh"

string SF09_OutcomeRecordToJson(const SF09_OutcomeRecord &o)
{
   return "{\"schema\":\""+SF01_EscapeJsonString(o.schema)+"\",\"outcome_id\":\""+SF01_EscapeJsonString(o.outcome_id)+
          "\",\"candidate_id\":\""+SF01_EscapeJsonString(o.candidate_id)+"\",\"event_id\":\""+SF01_EscapeJsonString(o.event_id)+
          "\",\"strategy_id\":\""+SF01_EscapeJsonString(o.strategy_id)+"\",\"symbol\":\""+SF01_EscapeJsonString(o.symbol)+
          "\",\"filled\":"+SF01_CanonicalBool(o.filled)+",\"exit_reason\":"+IntegerToString((int)o.exit_reason)+
          ",\"gross_r\":"+SF01_CanonicalDouble(o.gross_r)+",\"net_r\":"+SF01_CanonicalDouble(o.net_r)+
          ",\"mfe_r\":"+SF01_CanonicalDouble(o.mfe_r)+",\"mae_r\":"+SF01_CanonicalDouble(o.mae_r)+
          ",\"cost_r\":"+SF01_CanonicalDouble(o.costs.total_cost_r)+",\"path_hash\":\""+SF01_EscapeJsonString(o.path_hash)+"\"}";
}

#endif
