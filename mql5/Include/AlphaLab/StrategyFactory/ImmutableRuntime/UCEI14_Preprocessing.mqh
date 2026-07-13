#ifndef ALPHALAB_UCEI14_PREPROCESSING
#define ALPHALAB_UCEI14_PREPROCESSING
#include "UCEI14_Contracts.mqh"
float UCEI14F32(const double x){return((float)x);}
bool UCEI14Preprocess(const UCEI14Input &input,UCEI14Vector &out,string &reason){if(input.direction!="long"&&input.direction!="short"){reason="unknown_category";return(false);}double score=MathMax(0.0,MathMin(1.0,input.score));double liquidity=MathMax(0.0,MathMin(1.0,input.liquidity));out.values[0]=UCEI14F32((score-0.5)/0.25);out.values[1]=input.direction=="long"?1.0:0.0;out.values[2]=input.direction=="short"?1.0:0.0;out.values[3]=UCEI14F32(liquidity);out.values[4]=input.blocked?1.0:0.0;reason="";return(true);}
#endif
