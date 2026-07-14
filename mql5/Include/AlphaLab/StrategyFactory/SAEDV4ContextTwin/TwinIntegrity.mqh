#ifndef AL_SAED_V4_02_TWIN_INTEGRITY_MQH
#define AL_SAED_V4_02_TWIN_INTEGRITY_MQH
bool ALTwinHashPresent(const string value){return StringLen(value)==64;}
bool ALTwinReceiptValid(const string manifest_hash,const string snapshot_hash,const string root_hash){return ALTwinHashPresent(manifest_hash)&&ALTwinHashPresent(snapshot_hash)&&ALTwinHashPresent(root_hash);}
#endif
