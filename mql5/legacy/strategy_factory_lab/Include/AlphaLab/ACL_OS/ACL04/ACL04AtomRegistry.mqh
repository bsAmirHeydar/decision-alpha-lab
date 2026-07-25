#ifndef AL_ACL04_ATOM_REGISTRY_MQH
#define AL_ACL04_ATOM_REGISTRY_MQH

struct AL_ACL04_AtomDefinition
  {
   string atom_id;
   int    arity;
   bool   known_time_safe;
   bool   human_lane_allowed;
   bool   ai_lane_allowed;
   bool   baseline_lane_allowed;
   string value_type;
  };

struct AL_ACL04_ActionDefinition
  {
   string action_id;
   bool   execution_capability;
   bool   capital_capability;
  };

bool AL_ACL04_AtomIsResearchSafe(const AL_ACL04_AtomDefinition &atom)
  {
   return(StringLen(atom.atom_id)>0 && atom.arity>=0 && atom.known_time_safe);
  }

bool AL_ACL04_ActionIsNonAuthoritative(const AL_ACL04_ActionDefinition &action)
  {
   return(StringLen(action.action_id)>0 && !action.execution_capability && !action.capital_capability);
  }

#endif
