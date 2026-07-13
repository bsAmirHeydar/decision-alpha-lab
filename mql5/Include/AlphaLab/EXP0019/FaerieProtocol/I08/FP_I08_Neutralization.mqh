#ifndef FP_I08_NEUTRALIZATION_MQH
#define FP_I08_NEUTRALIZATION_MQH
#include "FP_I08_Contracts.mqh"
bool FP_I08_ShouldNeutralize(const FP_I08_WWContext &ctx,const string symbol,const int side,const datetime minute,const double extreme){if(ctx.state!=FP_I08_WW_CONFIRMED||minute<=ctx.confirmed_time||symbol!=ctx.protected_symbol||side!=ctx.side)return false;return side==0?extreme>=ctx.protected_reference_price:extreme<=ctx.protected_reference_price;}
#endif
