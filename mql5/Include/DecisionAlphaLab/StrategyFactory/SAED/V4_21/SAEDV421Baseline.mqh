#ifndef __DECISION_ALPHA_LAB_SAEDV421BASELINE_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421BASELINE_MQH__
bool SAEDV421BaselineNonInferior(const double candidate,const double baseline,const double allowed_delta){return candidate-baseline>=allowed_delta;}
#endif
