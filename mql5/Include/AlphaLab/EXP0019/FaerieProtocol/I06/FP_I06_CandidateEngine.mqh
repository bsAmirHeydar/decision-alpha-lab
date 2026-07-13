#ifndef __FP_I06_CANDIDATE_ENGINE_MQH__
#define __FP_I06_CANDIDATE_ENGINE_MQH__
#include "FP_I06_FirstSweepClassifier.mqh"
class FP_I06_CandidateEngine { public: static FP_I06_DIRECTION DirectionForSide(FP_I06_PRICE_SIDE side){return side==FP_I06_LOW ? FP_I06_BULLISH : FP_I06_BEARISH;} static bool CanCreate(FP_I06_SWEEP_OUTCOME o){return o==FP_I06_LEFT_FIRST || o==FP_I06_RIGHT_FIRST;} static FP_I06_CANDIDATE_STATE OnProtectedTouch(FP_I06_CANDIDATE_STATE s){return s==FP_I06_RAW_ACTIVE ? FP_I06_CANCELLED_SECOND_TOUCH : s;} static FP_I06_CANDIDATE_STATE OnDataBlocked(FP_I06_CANDIDATE_STATE s){return s==FP_I06_RAW_ACTIVE ? FP_I06_INVALID_DATA : s;} };
#endif
