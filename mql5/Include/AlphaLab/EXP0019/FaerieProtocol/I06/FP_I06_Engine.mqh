#ifndef __FP_I06_ENGINE_MQH__
#define __FP_I06_ENGINE_MQH__
#include "FP_I06_CandidateEngine.mqh"
class FP_I06_Engine { public: static bool SameMinuteHasNoOrder(){return FP_I06_FirstSweepClassifier::Outcome(FP_I06_BOTH_SAME_M1)==FP_I06_SYMMETRIC_SAME_M1;} static bool WWDeferred(){return !FP_I06_RelationRegistry::IsSupported(FP_I06_WW);} static bool NoRuntimeAuthority(){return true;} };
#endif
