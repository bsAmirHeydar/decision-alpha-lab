#ifndef ALPHALAB_UCEI14_CANONICAL
#define ALPHALAB_UCEI14_CANONICAL
string UCEI14StableDecisionKey(const string request_id,const string bundle_hash){return(request_id+"|"+bundle_hash);}
bool UCEI14HashLooksValid(const string value){if(StringLen(value)!=64)return(false);for(int i=0;i<64;i++){ushort c=StringGetCharacter(value,i);bool digit=(c>='0'&&c<='9');bool lower=(c>='a'&&c<='f');if(!digit&&!lower)return(false);}return(true);}
#endif
