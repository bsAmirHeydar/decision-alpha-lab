#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_CANONICAL_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_CANONICAL_MQH

string SAEDV4DslNormalizeIdentifier(const string value)
  {
   string result=value;
   StringTrimLeft(result);
   StringTrimRight(result);
   StringToLower(result);
   return result;
  }

bool SAEDV4DslLooksLikeSha256(const string value)
  {
   if(StringLen(value)!=64) return false;
   for(int i=0;i<StringLen(value);i++)
     {
      const ushort ch=StringGetCharacter(value,i);
      const bool digit=(ch>='0' && ch<='9');
      const bool lower=(ch>='a' && ch<='f');
      if(!digit && !lower) return false;
     }
   return true;
  }
#endif
