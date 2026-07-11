#ifndef __SF15_HASHING_MQH__
#define __SF15_HASHING_MQH__
string SF15_Fnv1aText(const string value)
  {
   ulong hash=0xcbf29ce484222325;
   uchar data[]; StringToCharArray(value,data,0,WHOLE_ARRAY,CP_UTF8);
   int count=ArraySize(data); if(count>0 && data[count-1]==0) count--;
   for(int i=0;i<count;i++){ hash^=(ulong)data[i]; hash*=0x100000001b3; }
   string output=StringFormat("%016I64X",hash);StringToLower(output);return output;
  }
string SF15_Fnv1aBytes(const uchar &data[])
  {
   ulong hash=0xcbf29ce484222325;
   for(int i=0;i<ArraySize(data);i++){ hash^=(ulong)data[i]; hash*=0x100000001b3; }
   string output=StringFormat("%016I64X",hash);StringToLower(output);return output;
  }
bool SF15_IsFinite(const double value){ return MathIsValidNumber(value) && value!=DBL_MAX && value!=-DBL_MAX; }
#endif
