#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_CANONICAL_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_CANONICAL_MQH

string SAEDHypergraphNormalizeToken(const string raw)
  {
   string value=raw;
   StringTrimLeft(value);
   StringTrimRight(value);
   StringToLower(value);
   return value;
  }

bool SAEDHypergraphIsHex64(const string value)
  {
   if(StringLen(value)!=64)
      return false;
   for(int index=0;index<StringLen(value);index++)
     {
      ushort code=StringGetCharacter(value,index);
      bool digit=(code>=48 && code<=57);
      bool lower=(code>=97 && code<=102);
      if(!digit && !lower)
         return false;
     }
   return true;
  }

string SAEDHypergraphStableDiagnosticId(const string prefix,const string payload)
  {
   uint hash=2166136261;
   for(int index=0;index<StringLen(payload);index++)
     {
      hash^=(uint)StringGetCharacter(payload,index);
      hash*=16777619;
     }
   return prefix+"_"+IntegerToString((int)hash);
  }

#endif
