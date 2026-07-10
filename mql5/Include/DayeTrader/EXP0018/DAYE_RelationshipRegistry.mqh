#ifndef __EXP0018_DAYE_RELATIONSHIP_REGISTRY_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_REGISTRY_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipTypes.mqh>

void DAYE_AppendRelationship(DAYE_RelationshipDefinition &items[],
                             const string relationship_id,
                             const string source_alias,
                             const DAYE_RelationshipFamily family,
                             const DAYE_RelationshipSelector selector,
                             const DAYE_PeriodId current_period_id,
                             const string current_period_code,
                             const DAYE_PeriodId reference_period_id,
                             const string reference_period_code,
                             const bool is_major,
                             const string chart_label,
                             const bool implementation_ready,
                             const string blocker_decision_id,
                             const string source_authority,
                             const string notes)
{
   int index = ArraySize(items);
   ArrayResize(items,index + 1);
   ZeroMemory(items[index]);
   items[index].schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   items[index].relationship_id = relationship_id;
   items[index].source_alias = source_alias;
   items[index].family = family;
   items[index].selector = selector;
   items[index].current_period_id = current_period_id;
   items[index].current_period_code = current_period_code;
   items[index].reference_period_id = reference_period_id;
   items[index].reference_period_code = reference_period_code;
   items[index].is_major = is_major;
   items[index].chart_label = chart_label;
   items[index].enabled_by_default = true;
   items[index].implementation_ready = implementation_ready;
   items[index].doctrine_status = implementation_ready ? DAYE_REL_DOCTRINE_READY : DAYE_REL_DOCTRINE_BLOCKED;
   items[index].blocker_decision_id = blocker_decision_id;
   items[index].source_authority = source_authority;
   items[index].notes = notes;
}

int DAYE_BuildCanonicalRelationshipRegistry(DAYE_RelationshipDefinition &items[])
{
   ArrayResize(items,0);

   // Six major relationships.
   DAYE_AppendRelationship(items,"DAYE_W_CURR_VS_W_PREV","WW",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_SAME_CODE,DAYE_PERIOD_W,"W",DAYE_PERIOD_W,"W",true,"WW",false,"DY-A03","Primary Word + Phase00 doctrine","Weekly boundary remains blocked until ADR-DY-A03 is accepted.");
   DAYE_AppendRelationship(items,"DAYE_D_CURR_VS_D_PREV","DD",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_SAME_CODE,DAYE_PERIOD_D,"D",DAYE_PERIOD_D,"D",true,"DD",true,"","Primary Word + Phase00 doctrine","Current Daye trading day versus previous Daye trading day.");
   DAYE_AppendRelationship(items,"DAYE_A_CURR_VS_P_PREV","PA",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_A,"A",DAYE_PERIOD_P,"P",true,"PA",true,"","Primary Word + Phase00 doctrine","Current A session versus immediately preceding P session.");
   DAYE_AppendRelationship(items,"DAYE_L_CURR_VS_A_PREV","AL",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_L,"L",DAYE_PERIOD_A,"A",true,"AL",true,"","Primary Word + Phase00 doctrine","Current L session versus immediately preceding A session.");
   DAYE_AppendRelationship(items,"DAYE_N_CURR_VS_L_PREV","LN",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_N,"N",DAYE_PERIOD_L,"L",true,"LN",true,"","Primary Word + Phase00 doctrine","Current N session versus immediately preceding L session.");
   DAYE_AppendRelationship(items,"DAYE_P_CURR_VS_N_PREV","NP",DAYE_REL_FAMILY_MAJOR,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_P,"P",DAYE_PERIOD_N,"N",true,"NP",false,"DY-A05","Primary Word + Phase00 proposed interpretation","NP remains blocked until ADR-DY-A05 is accepted.");

   // Sixteen 90-minute / tail relationships.
   DAYE_AppendRelationship(items,"DAYE_A1_VS_P4","p4a1",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_A1,"a1",DAYE_PERIOD_P4,"p4",false,"",true,"","Primary Word","Current a1 versus immediately preceding p4.");
   DAYE_AppendRelationship(items,"DAYE_A2_VS_A1","a1a2",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_A2,"a2",DAYE_PERIOD_A1,"a1",false,"",true,"","Primary Word","Current a2 versus a1.");
   DAYE_AppendRelationship(items,"DAYE_A3_VS_A2","a2a3",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_A3,"a3",DAYE_PERIOD_A2,"a2",false,"",true,"","Primary Word","Current a3 versus a2.");
   DAYE_AppendRelationship(items,"DAYE_A4_VS_A3","a3a4",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_A4,"a4",DAYE_PERIOD_A3,"a3",false,"",true,"","Primary Word","Current a4 versus a3.");

   DAYE_AppendRelationship(items,"DAYE_L1_VS_A4","a4l1",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_L1,"l1",DAYE_PERIOD_A4,"a4",false,"",true,"","Primary Word","Current l1 versus a4.");
   DAYE_AppendRelationship(items,"DAYE_L2_VS_L1","l1l2",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_L2,"l2",DAYE_PERIOD_L1,"l1",false,"",true,"","Primary Word","Current l2 versus l1.");
   DAYE_AppendRelationship(items,"DAYE_L3_VS_L2","l2l3",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_L3,"l3",DAYE_PERIOD_L2,"l2",false,"",true,"","Primary Word","Current l3 versus l2.");
   DAYE_AppendRelationship(items,"DAYE_L4_VS_L3","l3l4",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_L4,"l4",DAYE_PERIOD_L3,"l3",false,"",true,"","Primary Word","Current l4 versus l3.");

   DAYE_AppendRelationship(items,"DAYE_N1_VS_L4","l4n1",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_N1,"n1",DAYE_PERIOD_L4,"l4",false,"",true,"","Primary Word","Current n1 versus l4.");
   DAYE_AppendRelationship(items,"DAYE_N2_VS_N1","n1n2",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_N2,"n2",DAYE_PERIOD_N1,"n1",false,"",true,"","Primary Word","Current n2 versus n1.");
   DAYE_AppendRelationship(items,"DAYE_N3_VS_N2","n2n3",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_N3,"n3",DAYE_PERIOD_N2,"n2",false,"",true,"","Primary Word","Current n3 versus n2.");
   DAYE_AppendRelationship(items,"DAYE_N4_VS_N3","n3n4",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_N4,"n4",DAYE_PERIOD_N3,"n3",false,"",true,"","Primary Word","Current n4 versus n3.");

   DAYE_AppendRelationship(items,"DAYE_P1_VS_N4","n4p1",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_P1,"p1",DAYE_PERIOD_N4,"n4",false,"",true,"","Primary Word","Current p1 versus n4.");
   DAYE_AppendRelationship(items,"DAYE_P2_VS_P1","p1p2",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_P2,"p2",DAYE_PERIOD_P1,"p1",false,"",true,"","Primary Word","Current p2 versus p1.");
   DAYE_AppendRelationship(items,"DAYE_P3_VS_P2","p2p3",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_P3,"p3",DAYE_PERIOD_P2,"p2",false,"",true,"","Primary Word","Current p3 versus p2.");
   DAYE_AppendRelationship(items,"DAYE_P4_VS_P3","p3p4",DAYE_REL_FAMILY_MINOR_90M,DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL,DAYE_PERIOD_P4,"p4",DAYE_PERIOD_P3,"p3",false,"",true,"","Primary Word","Current p4 versus p3. p4 remains a thirty-minute tail.");

   return ArraySize(items);
}

bool DAYE_IsRelationshipEnabledByConfig(const DAYE_RelationshipDefinition &definition,
                                        const DAYE_RelationshipConfig &config)
{
   if(!definition.enabled_by_default)
      return false;
   if(definition.family == DAYE_REL_FAMILY_MAJOR)
      return config.enable_major_relationships;
   if(definition.family == DAYE_REL_FAMILY_MINOR_90M)
      return config.enable_minor_relationships;
   return false;
}

bool DAYE_FindRelationshipDefinition(const DAYE_RelationshipDefinition &items[],
                                     const string relationship_id,
                                     DAYE_RelationshipDefinition &definition)
{
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].relationship_id == relationship_id)
      {
         definition = items[i];
         return true;
      }
   }
   ZeroMemory(definition);
   return false;
}

bool DAYE_ValidateCanonicalRelationshipRegistry(const DAYE_RelationshipDefinition &items[],string &reason)
{
   reason = "";
   if(ArraySize(items) != 22)
   {
      reason = "relationship_registry_must_contain_exactly_22_records";
      return false;
   }

   int major_count = 0;
   int minor_count = 0;
   int blocked_count = 0;
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].schema_version != DAYE_RELATIONSHIP_SCHEMA_VERSION)
      {
         reason = "relationship_schema_version_mismatch";
         return false;
      }
      if(items[i].relationship_id == "" || items[i].source_alias == "")
      {
         reason = "relationship_identity_is_empty";
         return false;
      }
      if(items[i].current_period_id == DAYE_PERIOD_NONE || items[i].reference_period_id == DAYE_PERIOD_NONE)
      {
         reason = "relationship_period_identity_is_invalid";
         return false;
      }
      if(items[i].current_period_code == "" || items[i].reference_period_code == "")
      {
         reason = "relationship_period_code_is_empty";
         return false;
      }
      if(items[i].selector == DAYE_REL_SELECTOR_UNKNOWN)
      {
         reason = "relationship_selector_is_unknown";
         return false;
      }
      if(items[i].is_major)
         major_count++;
      else
         minor_count++;
      if(!items[i].implementation_ready)
         blocked_count++;

      for(int j=i+1;j<ArraySize(items);j++)
      {
         if(items[i].relationship_id == items[j].relationship_id)
         {
            reason = "duplicate_relationship_id";
            return false;
         }
         if(items[i].source_alias == items[j].source_alias)
         {
            reason = "duplicate_source_alias";
            return false;
         }
      }
   }

   if(major_count != 6)
   {
      reason = "major_relationship_count_must_equal_6";
      return false;
   }
   if(minor_count != 16)
   {
      reason = "minor_relationship_count_must_equal_16";
      return false;
   }
   if(blocked_count != 2)
   {
      reason = "blocked_relationship_count_must_equal_2";
      return false;
   }
   return true;
}

#endif
