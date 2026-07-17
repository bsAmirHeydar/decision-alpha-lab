#ifndef ALPHALAB_ACL05_BATCH_IDENTITY_MQH
#define ALPHALAB_ACL05_BATCH_IDENTITY_MQH
#include "ACL05Types.mqh"
struct ACL05BatchIdentity { string batch_id; string context_id; string context_version; string definition_digest; ENUM_ACL05_BATCH_STATE state; bool material_mutation_allowed; };
bool ACL05IsFrozen(const ACL05BatchIdentity &x){ return x.state==ACL05_BATCH_FROZEN && !x.material_mutation_allowed && StringLen(x.batch_id)>0 && StringLen(x.definition_digest)==71; }
#endif
