#ifndef UCEI08_ALGORITHM_DESCRIPTOR_MQH
#define UCEI08_ALGORITHM_DESCRIPTOR_MQH
#include "UCEI08_Enums.mqh"
struct UCEI08_AlgorithmDescriptor{
 string algorithm_id;string algorithm_version;string trainer_id;string trainer_version;UCEI08_AlgorithmFamily family;string task_csv;bool probability_output;bool supports_sample_weight;bool supports_missing_values;bool supports_multiclass;string determinism;string portability;string export_csv;string dependency_csv;string tags_csv;string limitations_csv;
 string Key()const{return algorithm_id+"@"+algorithm_version;}
 bool IsValid()const{return StringLen(algorithm_id)>0 && StringLen(algorithm_version)>0 && StringLen(trainer_id)>0 && StringLen(trainer_version)>0 && StringLen(task_csv)>0;}
};
#endif
