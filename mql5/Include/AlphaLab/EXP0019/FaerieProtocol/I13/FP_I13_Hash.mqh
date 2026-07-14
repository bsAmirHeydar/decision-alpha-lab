#ifndef __FP_I13_HASH_MQH__
#define __FP_I13_HASH_MQH__
ulong FP_I13_Hash64(const string value){ulong h=1469598103934665603;for(int i=0;i<StringLen(value);i++){h^=(ulong)StringGetCharacter(value,i);h*=1099511628211;}return h;}
string FP_I13_Hex64(ulong v){return StringFormat("%I64X",v);}
#endif
