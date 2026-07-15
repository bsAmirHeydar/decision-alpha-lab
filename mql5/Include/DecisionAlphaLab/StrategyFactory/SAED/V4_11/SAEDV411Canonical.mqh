#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_CANONICAL_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_CANONICAL_MQH__
bool SAEDV411IsSha256(const string value)
{
   if(StringLen(value)!=64) return false;
   for(int i=0;i<64;i++)
   {
      ushort c=StringGetCharacter(value,i);
      bool digit=(c>='0' && c<='9');
      bool lower=(c>='a' && c<='f');
      if(!digit && !lower) return false;
   }
   return true;
}
bool SAEDV411KnownTimeValid(const datetime event_time,const datetime known_time)
{
   return known_time>=event_time;
}
#endif
