#ifndef __UCE03_CANONICAL_CODEC_MQH__
#define __UCE03_CANONICAL_CODEC_MQH__

string UCE03_Hex4(const uint value)
{
   const string digits="0123456789abcdef";
   string result="";
   for(int shift=12;shift>=0;shift-=4)
      result+=StringSubstr(digits,(int)((value>>shift)&15),1);
   return result;
}

string UCE03_JsonEscapeAscii(const string value)
{
   string result="";
   const int count=StringLen(value);
   for(int i=0;i<count;i++)
   {
      const uint code=(uint)StringGetCharacter(value,i);
      if(code==34) result+="\\\"";
      else if(code==92) result+="\\\\";
      else if(code==8) result+="\\b";
      else if(code==9) result+="\\t";
      else if(code==10) result+="\\n";
      else if(code==12) result+="\\f";
      else if(code==13) result+="\\r";
      else if(code<32 || code>126) result+="\\u"+UCE03_Hex4(code&65535);
      else result+=StringSubstr(value,i,1);
   }
   return result;
}
string UCE03_JsonString(const string value){return "\""+UCE03_JsonEscapeAscii(value)+"\"";}
string UCE03_CanonicalBool(const bool value){return value?"true":"false";}
string UCE03_CanonicalNullableLong(const bool present,const long value){return present?IntegerToString(value):"null";}
string UCE03_CanonicalScaledInteger(const long units,const int scale)
{
   if(scale<0 || scale>18)return "";
   const bool negative=(units<0);
   ulong absolute=negative ? ((ulong)(-(units+1))+1) : (ulong)units;
   string digits=IntegerToString((long)absolute);
   if(scale==0)return (negative && absolute>0?"-":"")+digits;
   while(StringLen(digits)<=scale)digits="0"+digits;
   const int split=StringLen(digits)-scale;
   return (negative && absolute>0?"-":"")+StringSubstr(digits,0,split)+"."+StringSubstr(digits,split);
}

class CUCE03CanonicalObject
{
private:
   string m_keys[];
   string m_values[];
public:
   void Clear(){ArrayResize(m_keys,0);ArrayResize(m_values,0);}
   bool AddJson(const string key,const string canonical_json)
   {
      if(key=="" || canonical_json=="")return false;
      const int size=ArraySize(m_keys);
      for(int i=0;i<size;i++)if(m_keys[i]==key)return false;
      ArrayResize(m_keys,size+1);ArrayResize(m_values,size+1);
      m_keys[size]=key;m_values[size]=canonical_json;return true;
   }
   bool AddString(const string key,const string value){return AddJson(key,UCE03_JsonString(value));}
   bool AddLong(const string key,const long value){return AddJson(key,IntegerToString(value));}
   bool AddBool(const string key,const bool value){return AddJson(key,UCE03_CanonicalBool(value));}
   string Serialize()
   {
      const int size=ArraySize(m_keys);
      int order[];ArrayResize(order,size);
      for(int i=0;i<size;i++)order[i]=i;
      for(int i=0;i<size;i++)for(int j=i+1;j<size;j++)
         if(m_keys[order[j]]<m_keys[order[i]]){const int temp=order[i];order[i]=order[j];order[j]=temp;}
      string result="{";
      for(int i=0;i<size;i++)
      {
         if(i>0)result+=",";
         const int index=order[i];
         result+=UCE03_JsonString(m_keys[index])+":"+m_values[index];
      }
      return result+"}";
   }
};
#endif
