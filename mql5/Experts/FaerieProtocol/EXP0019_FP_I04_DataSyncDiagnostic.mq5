#property strict
#property version "1.00"
#include <FaerieProtocol/EXP0019/Data/FP_I04_All.mqh>
input string InpLeftSymbol="ES";
input string InpRightSymbol="NQ";
input int InpMinutes=60;
int OnInit(){if(InpMinutes<1)return INIT_PARAMETERS_INCORRECT;PrintFormat("FP-I04 diagnostic initialized left=%s right=%s minutes=%d authority=NONE",InpLeftSymbol,InpRightSymbol,InpMinutes);return INIT_SUCCEEDED;}
void OnTick(){}
