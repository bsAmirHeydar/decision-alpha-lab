#ifndef __UCEI09_ALGORITHM_DESCRIPTOR_MQH__
#define __UCEI09_ALGORITHM_DESCRIPTOR_MQH__
#include "UCEI09_Enums.mqh"
struct UCEI09_AlgorithmDescriptor{string algorithm_id;string algorithm_version;UCEI09_TASK_FAMILY family;string formulation;bool native_algorithm;string deterministic_level;string optional_dependency;string limitations;string Key()const{return algorithm_id+"@"+algorithm_version;}bool Valid()const{return algorithm_id!="" && algorithm_version!="" && formulation!="";}};
#endif
