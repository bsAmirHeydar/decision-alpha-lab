#ifndef ALPHALAB_UCEI15_CATALOG_MQH
#define ALPHALAB_UCEI15_CATALOG_MQH
int UCEI15_TreatmentFamilyCount(){return(9);}
int UCEI15_AlgorithmFamilyCount(){return(8);}
string UCEI15_TreatmentFamily(const int i){string x[9]={"tight_convex","wide_survival","limit","confirmation","fixed_target","runner","fixed_plus_trail","partial_plus_runner","capital_policy"};return(i>=0&&i<9?x[i]:"invalid");}
string UCEI15_AlgorithmFamily(const int i){string x[8]={"manual","naive","classical","ranking","treatment_choice","survival","distributional","deep"};return(i>=0&&i<8?x[i]:"invalid");}
#endif
