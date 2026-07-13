#ifndef __UCEI11_DAG_VALIDATION_MQH__
#define __UCEI11_DAG_VALIDATION_MQH__

#include "UCEI11_Contracts.mqh"

class CUCEI11DagValidation
  {
public:
   static bool UniqueNodeIds(const UCEI11_DagNode &nodes[])
     {
      for(int i=0; i<ArraySize(nodes); i++)
        {
         if(!nodes[i].Valid())
            return false;
         for(int j=0; j<i; j++)
            if(nodes[i].node_id==nodes[j].node_id)
               return false;
        }
      return true;
     }

   static bool BaselinePriorityBeforeChallenger(const int baseline_priority,const int challenger_priority)
     {
      return baseline_priority<challenger_priority;
     }

   static bool HiddenRoleExcluded(const string hidden_role,const string requested_roles_csv)
     {
      if(hidden_role=="")
         return false;
      string needle=","+hidden_role+",";
      string haystack=","+requested_roles_csv+",";
      return StringFind(haystack,needle)<0;
     }
  };

#endif
