#ifndef FP_SAEDV430AUTHORITY_MQH
#define FP_SAEDV430AUTHORITY_MQH
struct FP_SAEDV430Authority { bool promotion; bool runtime; bool risk_allocation; bool execution; bool production; bool online_learning; };
bool FP_SAEDV430AuthorityIsZero(const FP_SAEDV430Authority &value) { return(!value.promotion && !value.runtime && !value.risk_allocation && !value.execution && !value.production && !value.online_learning); }
#endif
