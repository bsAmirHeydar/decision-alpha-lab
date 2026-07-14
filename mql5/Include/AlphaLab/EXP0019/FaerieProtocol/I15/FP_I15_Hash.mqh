#ifndef FP_I15_HASH_MQH
#define FP_I15_HASH_MQH
string FP_I15_HashText(const string value){ uint h=2166136261; for(int i=0;i<StringLen(value);i++){ h^=(uint)StringGetCharacter(value,i); h*=16777619; } return StringFormat("%08X",h); }
string FP_I15_Id(const string prefix,const string payload){ return prefix+"-"+FP_I15_HashText(payload); }
#endif
