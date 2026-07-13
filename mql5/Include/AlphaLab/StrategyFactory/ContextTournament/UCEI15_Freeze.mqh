#ifndef ALPHALAB_UCEI15_FREEZE_MQH
#define ALPHALAB_UCEI15_FREEZE_MQH
bool UCEI15_FreezePass(const long declared_ms,const long outcome_cut_ms,const bool locked,const bool final_test_sealed){return(declared_ms<=outcome_cut_ms&&locked&&final_test_sealed);}
#endif
