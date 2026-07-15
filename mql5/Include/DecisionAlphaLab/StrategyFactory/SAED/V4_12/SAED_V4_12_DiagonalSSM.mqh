#ifndef SAED_V4_12_DIAGONAL_SSM_MQH
#define SAED_V4_12_DIAGONAL_SSM_MQH
#include "SAED_V4_12_Types.mqh"
bool SAEDV412DiagonalStep(const double &input[],const double dt_seconds,SAEDV412State &state){ if(ArraySize(input)!=12 || dt_seconds<=0.0) return false; for(int i=0;i<10;i++){ const double decay=MathExp(-0.01*dt_seconds/60.0); state.hidden[i]=MathTanh(decay*state.hidden[i]+(1.0-decay)*input[i%12]); } state.step_count++; return true; }
#endif
