#ifndef ALPHALAB_QUALIFICATION_KILL_SWITCH_MQH
#define ALPHALAB_QUALIFICATION_KILL_SWITCH_MQH
struct ALKillSwitchState { bool engaged; string reason_code; long engaged_at_ms; string generation_hash; };
bool ALKillSwitchBlocksActions(const ALKillSwitchState &state){ return state.engaged; }
bool ALEngageKillSwitch(ALKillSwitchState &state,const string reason_code,const long now_ms,const string generation_hash){ if(StringLen(reason_code)==0 || StringLen(generation_hash)!=64) return false; state.engaged=true; state.reason_code=reason_code; state.engaged_at_ms=now_ms; state.generation_hash=generation_hash; return true; }
#endif
