#ifndef SAEDV416_DIGEST_MQH
#define SAEDV416_DIGEST_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416DigestShapeValid(const string digest){if(StringLen(digest)!=64)return false;for(int i=0;i<64;i++){ushort c=StringGetCharacter(digest,i);if(!((c>='0'&&c<='9')||(c>='a'&&c<='f')))return false;}return true;}
#endif
