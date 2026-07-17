#ifndef SAED_V4_27_CONTRACTS_MQH
#define SAED_V4_27_CONTRACTS_MQH
bool SAEDV427IsProtectedRole(const int role){ return role==V427_HIDDEN_EVALUATION || role==V427_PROTECTED_FINAL; }
bool SAEDV427ResearchOnly(){ return true; }
#endif
