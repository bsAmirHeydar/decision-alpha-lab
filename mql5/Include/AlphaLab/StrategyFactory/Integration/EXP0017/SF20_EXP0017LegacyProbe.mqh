#ifndef __SF20_EXP0017_LEGACY_PROBE_MQH__
#define __SF20_EXP0017_LEGACY_PROBE_MQH__
#include "SF20_EXP0017Contracts.mqh"
#include <IntermarketDivergenceExecution/CG/CGD_DivergenceField.mqh>
#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>
class CSF20EXP0017LegacyProbe
{
private:SF20_EXP0017Config m_config;SCGTGroupDef m_groups[CGT_GROUP_COUNT];CCGT_TimeAnatomy m_time;CCGD_DivergenceField m_field;bool m_ready;
 void SetGroup(const int i,const ECGTGroupId id,const string name,const int minutes){m_groups[i].id=id;m_groups[i].name=name;m_groups[i].minutes=minutes;m_groups[i].enabled=SF20_GroupEnabled(m_config.group_mask,i);}
 void BuildRegistry(){SetGroup(CGT_CG3M,CGT_CG3M,"cg_3m",3);SetGroup(CGT_CG5M,CGT_CG5M,"cg_5m",5);SetGroup(CGT_CG9M,CGT_CG9M,"cg_9m",9);SetGroup(CGT_CG10M,CGT_CG10M,"cg_10m",10);SetGroup(CGT_CG15M,CGT_CG15M,"cg_15m",15);SetGroup(CGT_CG18M,CGT_CG18M,"cg_18m",18);SetGroup(CGT_CG20M,CGT_CG20M,"cg_20m",20);SetGroup(CGT_CG24M,CGT_CG24M,"cg_24m",24);SetGroup(CGT_CG30M,CGT_CG30M,"cg_30m",30);SetGroup(CGT_CG40M,CGT_CG40M,"cg_40m",40);SetGroup(CGT_CG45M,CGT_CG45M,"cg_45m",45);SetGroup(CGT_CG60M,CGT_CG60M,"cg_60m",60);SetGroup(CGT_CG72M,CGT_CG72M,"cg_72m",72);SetGroup(CGT_CG90M,CGT_CG90M,"cg_90m",90);SetGroup(CGT_CG120M,CGT_CG120M,"cg_120m",120);SetGroup(CGT_CG150M,CGT_CG150M,"cg_150m",150);SetGroup(CGT_CG180M,CGT_CG180M,"cg_180m",180);SetGroup(CGT_CG240M,CGT_CG240M,"cg_240m",240);SetGroup(CGT_CG300M,CGT_CG300M,"cg_300m",300);SetGroup(CGT_CG360M,CGT_CG360M,"cg_360m",360);SetGroup(CGT_CG720M,CGT_CG720M,"cg_720m",720);}
public:CSF20EXP0017LegacyProbe(){m_ready=false;}
 bool Configure(const SF20_EXP0017Config &config,string &error)
 {
  if(!SF20_ValidateEXP0017Config(config,error))return false;m_config=config;BuildRegistry();SCGTTimeConfig tc;tc.broker_utc_offset_hours=config.broker_utc_offset_hours;tc.use_auto_new_york_dst=config.use_auto_new_york_dst;tc.manual_new_york_utc_offset_hours=config.manual_new_york_utc_offset_hours;tc.max_previous_cycles_shown=10000;m_time.Configure(tc);SCGDDivergenceConfig dc;dc.symbol_a=config.symbol_a;dc.symbol_b=config.symbol_b;dc.broker_utc_offset_hours=config.broker_utc_offset_hours;dc.max_groups_shown=CGT_GROUP_COUNT;dc.max_candidates_per_group_shown=10000;dc.require_m1_history=config.require_m1_history;dc.show_only_groups_with_divergence=false;dc.show_prices=false;dc.show_symmetric_no_divergence_counts=true;m_field.Configure(dc);m_ready=true;error="";return true;
 }
 int Observe(const datetime broker_now,const long observed_at_utc_msc,SCGDDivergenceCandidate &out[],SF20_EXP0017GroupEvidence &groups[],string &error)
 {
  ArrayResize(out,0);ArrayResize(groups,0);if(!m_ready){error="legacy probe not configured";return 0;}SCGTTimeSnapshot ts;if(!m_time.BuildTimeSnapshot(broker_now,ts)){error="legacy time snapshot failed";return 0;}
  for(int i=0;i<CGT_GROUP_COUNT;i++){if(!m_groups[i].enabled)continue;SCGTCycleSnapshot cycle;if(!m_time.BuildCycleSnapshot(ts,m_groups[i],cycle))continue;SCGDDivergenceCandidate candidates[];SCGDGroupDivergenceState state;int count=m_field.BuildDivergencesForGroup(ts,cycle,candidates,state);int g=ArraySize(groups);ArrayResize(groups,g+1);groups[g].group_name=state.group_name;groups[g].group_minutes=state.group_minutes;groups[g].candidate_count=count;groups[g].missing_data_count=state.missing_data_count;groups[g].symmetric_high_count=state.symmetric_high_no_divergence_count;groups[g].symmetric_low_count=state.symmetric_low_no_divergence_count;groups[g].observed_at_utc_msc=observed_at_utc_msc;groups[g].evidence_hash=SF01_StableId("sf20group",state.group_name+"|"+IntegerToString(count)+"|"+IntegerToString(state.missing_data_count)+"|"+IntegerToString(observed_at_utc_msc));if(count>0){int start=ArraySize(out);ArrayResize(out,start+count);for(int c=0;c<count;c++)out[start+c]=candidates[c];}}
  error="";return ArraySize(out);
 }
};
#endif
