#ifndef __FP_I12_HASH_MQH__
#define __FP_I12_HASH_MQH__
string FP_I12_Hash(const string value){uint h=2166136261;for(int i=0;i<StringLen(value);i++){h^=(uint)StringGetCharacter(value,i);h*=16777619;}return StringFormat("%08X",h);}
string FP_I12_ShortName(const string ns,const string kind,const string semantic){return "FP12::"+FP_I12_Hash(ns)+"::"+kind+"::"+FP_I12_Hash(semantic);}
#endif
