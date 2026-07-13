#ifndef ALPHALAB_UCEI14_MODEL
#define ALPHALAB_UCEI14_MODEL
#include "UCEI14_Preprocessing.mqh"
double UCEI14Exp(const double x){return(MathExp(x));}
bool UCEI14Infer(const UCEI14Vector &x,UCEI14Output &out){double a=(float)((float)((float)((float)((float)(x.values[0]*1.0)+(float)(x.values[1]*1.0))+(float)(x.values[2]*-2.0))+(float)(x.values[3]*0.2))+(float)(x.values[4]*-5.0));double b=(float)((float)((float)((float)((float)(x.values[0]*-1.0)+(float)(x.values[1]*-1.0))+(float)(x.values[2]*2.0))+(float)(x.values[3]*-0.2))+(float)(x.values[4]*5.0));double m=MathMax(a,b);double ea=UCEI14Exp(a-m),eb=UCEI14Exp(b-m),s=ea+eb;out.enter_long=(float)(ea/s);out.no_action=(float)(eb/s);out.label=(out.enter_long>=out.no_action)?"enter_long":"no_action";return(true);}
#endif
