#ifndef __FP_I10_HASH_MQH__
#define __FP_I10_HASH_MQH__
ulong FP_I10_Fnv1a64(const string value){ ulong h=1469598103934665603; for(int i=0;i<StringLen(value);i++){ h^=(ulong)StringGetCharacter(value,i); h*=1099511628211; } return h; }
string FP_I10_Hex64(const ulong value){ return StringFormat("%016I64X",value); }
string FP_I10_StableId(const string prefix,const string material){ return prefix+"_"+FP_I10_Hex64(FP_I10_Fnv1a64(material)); }
#endif
