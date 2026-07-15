#ifndef SAED_V4_12_RESET_MQH
#define SAED_V4_12_RESET_MQH
#include "SAED_V4_12_Types.mqh"
void SAEDV412Reset(SAEDV412State &state){ for(int i=0;i<10;i++) state.hidden[i]=0.0; state.step_count=0; state.state_hash=""; }
#endif
