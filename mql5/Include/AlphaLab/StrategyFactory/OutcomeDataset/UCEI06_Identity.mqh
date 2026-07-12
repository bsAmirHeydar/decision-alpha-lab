#ifndef ALPHALAB_UCEI06_IDENTITY_MQH
#define ALPHALAB_UCEI06_IDENTITY_MQH
uint UCEI06_Fnv1a(const string value){uchar bytes[];StringToCharArray(value,bytes,0,WHOLE_ARRAY,CP_UTF8);uint h=2166136261;int n=ArraySize(bytes);if(n>0 && bytes[n-1]==0)n--;for(int i=0;i<n;i++){h^=(uint)bytes[i];h*=16777619;}return h;}
string UCEI06_Hex8(const uint value){string digits="0123456789abcdef";string out="";for(int shift=28;shift>=0;shift-=4)out+=StringSubstr(digits,(int)((value>>shift)&15),1);return out;}
string UCEI06_StableId(const string prefix,const string material){return prefix+"_"+UCEI06_Hex8(UCEI06_Fnv1a(material));}
#endif
