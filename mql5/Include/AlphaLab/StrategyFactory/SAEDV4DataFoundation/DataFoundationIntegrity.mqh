#ifndef __AL_SAED_V4_DATA_FOUNDATION_INTEGRITY_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_INTEGRITY_MQH__
class ALDataIntegrityGate {
public:
 static bool HashLooksValid(const string value){
   if(StringLen(value)!=64)return false;
   for(int i=0;i<64;i++){
     ushort c=StringGetCharacter(value,i);
     bool digit=(c>='0' && c<='9'); bool lower=(c>='a' && c<='f');
     if(!digit && !lower)return false;
   }
   return true;
 }
};
#endif
