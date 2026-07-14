#ifndef __ALPHALAB_SAEDV400_CONTRACTS_MQH__
#define __ALPHALAB_SAEDV400_CONTRACTS_MQH__
#include "SAEDV400_Enums.mqh"

struct SAEDV400_Actor
  {
   string actor_id;
   ENUM_SAEDV400_ACTOR_TYPE actor_type;
   string organization_unit;
  };

struct SAEDV400_AuthorityRequest
  {
   string program_id;
   SAEDV400_Actor actor;
   ENUM_SAEDV400_AUTHORITY authority;
   datetime known_time;
   string purpose;
  };

struct SAEDV400_EvidenceRequest
  {
   string program_id;
   SAEDV400_Actor actor;
   ENUM_SAEDV400_EVIDENCE_ROLE evidence_role;
   ENUM_SAEDV400_EVIDENCE_OPERATION operation;
   datetime known_time;
   bool synthetic;
   bool positive_promotion_claim;
  };

struct SAEDV400_Decision
  {
   ENUM_SAEDV400_DECISION_STATUS status;
   string reason_code;
   string detail;
  };

#endif
