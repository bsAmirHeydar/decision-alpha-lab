#ifndef __FP_I06_RELATION_REGISTRY_MQH__
#define __FP_I06_RELATION_REGISTRY_MQH__
#include "FP_I06_Contracts.mqh"
class FP_I06_RelationRegistry { public: static int RelationCount(){return 7;} static int SupportedCount(){return 6;} static bool IsSupported(FP_I06_RELATION r){return r!=FP_I06_WW;} static string Code(FP_I06_RELATION r){string values[7]={"AL","AN","LN","NA","NL","NN","WW"};return values[(int)r];} static string ReferenceKind(FP_I06_RELATION r){string values[7]={"A","A","L","N","N","N","W"};return values[(int)r];} static string CheckKind(FP_I06_RELATION r){string values[7]={"L","N","N","A","L","N","W"};return values[(int)r];} static bool Historical(FP_I06_RELATION r){return r==FP_I06_NA || r==FP_I06_NL || r==FP_I06_NN;} };
#endif
