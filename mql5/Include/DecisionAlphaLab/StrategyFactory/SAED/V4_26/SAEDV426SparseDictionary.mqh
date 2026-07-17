#ifndef DAL_SAED_V426_SPARSE_DICTIONARY_MQH
#define DAL_SAED_V426_SPARSE_DICTIONARY_MQH
double SAEDV426SquaredError(const double observed,const double reconstructed){ double d=observed-reconstructed; return d*d; }
#endif
