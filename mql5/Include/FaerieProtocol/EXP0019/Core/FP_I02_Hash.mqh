#ifndef __EXP0019_FP_I02_HASH_MQH__
#define __EXP0019_FP_I02_HASH_MQH__

string FP_I02_BytesToHex(const uchar &bytes[])
  {
   string result="";
   for(int i=0;i<ArraySize(bytes);i++) result+=StringFormat("%02x",(int)bytes[i]);
   return result;
  }

string FP_I02_SHA256(const string text)
  {
   uchar data[],key[],digest[];
   int count=StringToCharArray(text,data,0,WHOLE_ARRAY,CP_UTF8);
   if(count>0 && data[count-1]==0) ArrayResize(data,count-1);
   ArrayResize(key,0);
   if(CryptEncode(CRYPT_HASH_SHA256,data,key,digest)<=0) return "";
   return FP_I02_BytesToHex(digest);
  }

string FP_I02_CompactId(const string prefix,const string canonical_material)
  {
   string digest=FP_I02_SHA256(canonical_material);
   if(StringLen(digest)!=64) return "";
   return prefix+"_"+StringSubstr(digest,0,32);
  }

bool FP_I02_IsLowerSha256(const string value)
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

#endif
