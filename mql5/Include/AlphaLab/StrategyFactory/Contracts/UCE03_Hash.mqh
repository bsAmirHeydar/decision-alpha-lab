#ifndef __UCE03_HASH_MQH__
#define __UCE03_HASH_MQH__
ulong UCE03_Fnv1a64Utf8(const string value)
{
   uchar bytes[];
   const int count=StringToCharArray(value,bytes,0,-1,CP_UTF8);
   ulong result=(((ulong)0xCBF29CE4)<<32)|(ulong)0x84222325;
   const ulong prime=(((ulong)0x00000100)<<32)|(ulong)0x000001B3;
   const int effective=(count>0 && bytes[count-1]==0)?count-1:count;
   for(int i=0;i<effective;i++){result^=(ulong)bytes[i];result*=prime;}
   return result;
}
string UCE03_UlongHex16(const ulong value)
{
   const string digits="0123456789abcdef";string result="";
   for(int i=15;i>=0;i--)result+=StringSubstr(digits,(int)((value>>(i*4))&15),1);
   return result;
}
string UCE03_Fnv1a64HexUtf8(const string value){return UCE03_UlongHex16(UCE03_Fnv1a64Utf8(value));}
#endif
