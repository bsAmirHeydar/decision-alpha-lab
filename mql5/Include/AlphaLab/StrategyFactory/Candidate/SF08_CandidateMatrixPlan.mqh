#ifndef __SF08_CANDIDATE_MATRIX_PLAN_MQH__
#define __SF08_CANDIDATE_MATRIX_PLAN_MQH__
#include "SF08_PolicyRegistry.mqh"

class CSF08CandidateMatrixPlan
{
private:
   SF08_CandidateTemplate m_templates[];
   bool m_compiled;
   string m_plan_hash;
public:
   string plan_id;
   string plan_version;
   CSF08CandidateMatrixPlan(void){ArrayResize(m_templates,0);m_compiled=false;m_plan_hash="";plan_id="";plan_version="";}
   int Count(void)const{return ArraySize(m_templates);} bool Compiled(void)const{return m_compiled;} string PlanHash(void)const{return m_plan_hash;}
   bool Add(const SF08_CandidateTemplate &input,string &error)
   {
      if(m_compiled){error="candidate matrix already compiled";return false;}
      if(ArraySize(m_templates)>=SF08_MAX_MATRIX_TEMPLATES){error="candidate matrix capacity exceeded";return false;}
      SF08_CandidateTemplate t=input;
      t.entry_parameters.parameter_hash=SF08_DerivePolicyParameterHash(t.entry_parameters);
      t.stop_parameters.parameter_hash=SF08_DerivePolicyParameterHash(t.stop_parameters);
      t.exit_parameters.parameter_hash=SF08_DerivePolicyParameterHash(t.exit_parameters);
      t.template_hash=SF08_DeriveCandidateTemplateHash(t);
      if(!SF08_ValidateCandidateTemplate(t,error))return false;
      for(int i=0;i<ArraySize(m_templates);i++)
         if(m_templates[i].template_id==t.template_id && m_templates[i].template_version==t.template_version)
         {error="duplicate candidate template identity";return false;}
      const int n=ArraySize(m_templates);ArrayResize(m_templates,n+1);m_templates[n]=t;error="";return true;
   }
   bool At(const int index,SF08_CandidateTemplate &t)const{if(index<0||index>=ArraySize(m_templates))return false;t=m_templates[index];return true;}
   bool Compile(const CSF08PolicyRegistry &registry,string &error)
   {
      if(!registry.Compiled()){error="policy registry not compiled";return false;}
      if(!SF01_IsSafeIdentifier(plan_id,128)||!SF01_IsSafeIdentifier(plan_version,64)){error="invalid matrix plan identity";return false;}
      if(ArraySize(m_templates)<=0){error="candidate matrix is empty";return false;}
      // stable insertion sort by priority, then template id
      for(int i=1;i<ArraySize(m_templates);i++)
      {
         SF08_CandidateTemplate key=m_templates[i];int j=i-1;
         while(j>=0 && (m_templates[j].priority>key.priority || (m_templates[j].priority==key.priority && m_templates[j].template_id>key.template_id)))
         {m_templates[j+1]=m_templates[j];j--;}
         m_templates[j+1]=key;
      }
      string canonical=plan_id+"|"+plan_version+"|"+registry.RegistryHash();
      for(int i=0;i<ArraySize(m_templates);i++)
      {
         SF08_CandidateTemplate t=m_templates[i];
         if(CheckPointer(registry.ResolveEntry(t.entry_policy_id,t.entry_policy_version))==POINTER_INVALID ||
            CheckPointer(registry.ResolveStop(t.stop_policy_id,t.stop_policy_version))==POINTER_INVALID ||
            CheckPointer(registry.ResolveExit(t.exit_policy_id,t.exit_policy_version))==POINTER_INVALID)
         {error="candidate template references unresolved policy";return false;}
         canonical+="|"+t.template_hash;
      }
      m_plan_hash=SF01_StableId("cmat",canonical);m_compiled=true;error="";return true;
   }
};

#endif
