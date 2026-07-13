#ifndef FP_I08_COMPILER_MQH
#define FP_I08_COMPILER_MQH
bool FP_I08_CompileWW(const string previous_week_id,const string current_week_id,string &reason){if(previous_week_id==""||current_week_id==""||previous_week_id==current_week_id){reason="FP_WRC_WEEK_INPUT_INVALID";return false;}reason="FP_WRC_WW_RELATION_COMPILED";return true;}
#endif
