#ifndef ALPHALAB_OPERATIONS_HASH_GUARD_MQH
#define ALPHALAB_OPERATIONS_HASH_GUARD_MQH
bool ALOpsIsLowerHex(const ushort code){ return (code>=(ushort)'0' && code<=(ushort)'9') || (code>=(ushort)'a' && code<=(ushort)'f'); }
bool ALOpsIsSha256(const string value){ if(StringLen(value)!=64) return false; for(int i=0;i<64;i++){ if(!ALOpsIsLowerHex(StringGetCharacter(value,i))) return false; } return true; }
#endif
