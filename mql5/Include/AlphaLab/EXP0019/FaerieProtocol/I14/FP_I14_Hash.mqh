#ifndef __FP_I14_HASH_MQH__
#define __FP_I14_HASH_MQH__
string FP_I14_HashText(const string value){ uint h=2166136261; for(int i=0;i<StringLen(value);i++){ h^=(uint)StringGetCharacter(value,i); h*=16777619; } return StringFormat("%08X",h); }
string FP_I14_EventFingerprint(const FP_I14_TraceEvent &e){ return FP_I14_HashText((string)e.sequence+"|"+(string)e.event_type+"|"+e.semantic_id+"|"+e.payload_hash+"|"+e.config_hash+"|"+e.source_revision_id+"|"+e.state+"|"+(string)e.buffer_index+"|"+DoubleToString(e.numeric_value,10)); }
#endif
