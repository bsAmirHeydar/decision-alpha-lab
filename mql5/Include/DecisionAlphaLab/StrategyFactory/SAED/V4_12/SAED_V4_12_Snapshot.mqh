#ifndef SAED_V4_12_SNAPSHOT_MQH
#define SAED_V4_12_SNAPSHOT_MQH
#include "SAED_V4_12_Types.mqh"
bool SAEDV412SnapshotValid(const SAEDV412State &state){ return state.step_count>=0 && StringLen(state.state_hash)>0; }
#endif
