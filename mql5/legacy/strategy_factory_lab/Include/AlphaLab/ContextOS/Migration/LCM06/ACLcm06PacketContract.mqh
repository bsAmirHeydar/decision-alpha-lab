#ifndef __ALPHALAB_LCM06_PACKET_CONTRACT_MQH__
#define __ALPHALAB_LCM06_PACKET_CONTRACT_MQH__
struct AL_LCM06_PACKET_CONTRACT { string packet_id; string identity_id; string source_path; string source_sha256; string target_path; bool owner_resolved; bool known_time_safe; bool security_reviewed; bool authority_denied; };
#endif
