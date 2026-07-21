#ifndef ALPHALAB_RTHP_ACL03_STATIC_MIRROR_MQH
#define ALPHALAB_RTHP_ACL03_STATIC_MIRROR_MQH

// Generated diagnostic mirror. It carries no detector runtime, order, or capital authority.
#define RTHP_CONTEXT_VERSION "1.0.2"
#define RTHP_ACL03_CLAIM_CEILING "CONTEXT_COMPILATION_REFERENCE_ONLY"
#define RTHP_ACL03_ANCHOR_TIME_ALIAS "confirmation_close_time"
#define RTHP_ACL03_DIRECTION_ALIAS "relation_polarity"
#define RTHP_ACL03_SUBJECT_KEY_ALIAS "symbol_pair_id"
#define RTHP_ACL03_DETECTOR_IR_DIGEST "sha256:643d1e6aedaaef33c73de4b04fd23d94ba291af8a0e8f9e9942e73059c9334fb"
#define RTHP_ACL03_OCCURRENCE_IR_DIGEST "sha256:22029214ddc97c8e94c65e23120de8e484f05afb884c617fc615d96b104d485b"
#define RTHP_ACL03_KNOWN_TIME_IR_DIGEST "sha256:1a80fa97f50f0e92ab9f2e3f03b6b435ccd17d5451a64d7568754cb87398c09f"

struct RTHP_ACL03IdentityProjection
  {
   datetime anchor_time;
   string direction;
   string subject_key;
   datetime confirmation_close_time;
   string relation_polarity;
   string symbol_pair_id;
  };

bool RTHP_ACL03IdentityAliasesAreConsistent(const RTHP_ACL03IdentityProjection &identity)
  {
   return(identity.anchor_time==identity.confirmation_close_time &&
          identity.direction==identity.relation_polarity &&
          identity.subject_key==identity.symbol_pair_id);
  }

#endif
