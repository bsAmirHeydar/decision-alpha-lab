#ifndef ALPHALAB_UCEI14_PARITY
#define ALPHALAB_UCEI14_PARITY
#include "UCEI14_Model.mqh"
bool UCEI14WithinTolerance(const double a,const double b,const double abs_tol,const double rel_tol){double ae=MathAbs(a-b);double denom=MathMax(MathMax(MathAbs(a),MathAbs(b)),1e-12);return(ae<=abs_tol||(ae/denom)<=rel_tol);}
bool UCEI14ParityVector(const UCEI14Input &input,const double expected_enter,const string expected_label,string &reason){UCEI14Vector x;UCEI14Output y;if(!UCEI14Preprocess(input,x,reason))return(false);if(!UCEI14Infer(x,y)){reason="inference_failure";return(false);}if(!UCEI14WithinTolerance(y.enter_long,expected_enter,1e-6,1e-5)){reason="numerical_tolerance_exceeded";return(false);}if(y.label!=expected_label){reason="decision_mismatch";return(false);}reason="";return(true);}
#endif
