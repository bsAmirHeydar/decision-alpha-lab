#ifndef __SF09_COST_MODEL_MQH__
#define __SF09_COST_MODEL_MQH__
#include "SF09_OutcomeEnums.mqh"
#include "../Contracts/SF01_AllContracts.mqh"

struct SF09_CostModelDescriptor
{
   string model_id;
   string version;
   bool deterministic;
   bool uses_observed_spread;
   string descriptor_hash;
};

struct SF09_CostRequest
{
   string candidate_id;
   ENUM_SF01_DIRECTION direction;
   double entry_price;
   double exit_price;
   double initial_risk_points;
   double observed_entry_spread_points;
   double observed_exit_spread_points;
   double point_size;
};

struct SF09_CostBreakdown
{
   string model_id;
   string model_version;
   double entry_spread_points;
   double exit_spread_points;
   double entry_slippage_points;
   double exit_slippage_points;
   double commission_r;
   double other_r;
   double total_cost_points;
   double total_cost_r;
   string cost_hash;
};

string SF09_CostBreakdownCanonical(const SF09_CostBreakdown &c)
{
   return c.model_id+"|"+c.model_version+"|"+SF01_CanonicalDouble(c.entry_spread_points)+"|"+
          SF01_CanonicalDouble(c.exit_spread_points)+"|"+SF01_CanonicalDouble(c.entry_slippage_points)+"|"+
          SF01_CanonicalDouble(c.exit_slippage_points)+"|"+SF01_CanonicalDouble(c.commission_r)+"|"+
          SF01_CanonicalDouble(c.other_r)+"|"+SF01_CanonicalDouble(c.total_cost_points)+"|"+
          SF01_CanonicalDouble(c.total_cost_r);
}
string SF09_DeriveCostHash(const SF09_CostBreakdown &c)
{return SF01_StableId("cost",SF09_CostBreakdownCanonical(c));}

class ISF09CostModel
{
public:
   virtual bool Descriptor(SF09_CostModelDescriptor &descriptor) const=0;
   virtual bool Compute(const SF09_CostRequest &request,SF09_CostBreakdown &cost,string &error) const=0;
};

class CSF09FixedCostModel : public ISF09CostModel
{
private:
   string m_model_id;
   string m_version;
   bool m_use_observed_spread;
   double m_entry_spread_points;
   double m_exit_spread_points;
   double m_entry_slippage_points;
   double m_exit_slippage_points;
   double m_commission_r;
   double m_other_r;
public:
   CSF09FixedCostModel(void)
   {
      m_model_id="sf09.cost.fixed"; m_version="1.0.0"; m_use_observed_spread=true;
      m_entry_spread_points=0.0; m_exit_spread_points=0.0;
      m_entry_slippage_points=0.0; m_exit_slippage_points=0.0;
      m_commission_r=0.0; m_other_r=0.0;
   }
   void Configure(const string model_id,const string version,const bool use_observed_spread,
                  const double entry_spread_points,const double exit_spread_points,
                  const double entry_slippage_points,const double exit_slippage_points,
                  const double commission_r,const double other_r)
   {
      m_model_id=model_id; m_version=version; m_use_observed_spread=use_observed_spread;
      m_entry_spread_points=entry_spread_points; m_exit_spread_points=exit_spread_points;
      m_entry_slippage_points=entry_slippage_points; m_exit_slippage_points=exit_slippage_points;
      m_commission_r=commission_r; m_other_r=other_r;
   }
   virtual bool Descriptor(SF09_CostModelDescriptor &d) const
   {
      d.model_id=m_model_id; d.version=m_version; d.deterministic=true; d.uses_observed_spread=m_use_observed_spread;
      d.descriptor_hash=SF01_StableId("cmdl",m_model_id+"|"+m_version+"|"+SF01_CanonicalBool(m_use_observed_spread));
      return true;
   }
   virtual bool Compute(const SF09_CostRequest &r,SF09_CostBreakdown &c,string &error) const
   {
      if(r.initial_risk_points<=0.0 || !MathIsValidNumber(r.initial_risk_points))
      { error="invalid risk points for cost model"; return false; }
      c.model_id=m_model_id; c.model_version=m_version;
      c.entry_spread_points=m_use_observed_spread?r.observed_entry_spread_points:m_entry_spread_points;
      c.exit_spread_points=m_use_observed_spread?r.observed_exit_spread_points:m_exit_spread_points;
      if(c.entry_spread_points<0.0)c.entry_spread_points=0.0;
      if(c.exit_spread_points<0.0)c.exit_spread_points=0.0;
      c.entry_slippage_points=m_entry_slippage_points;
      c.exit_slippage_points=m_exit_slippage_points;
      c.commission_r=m_commission_r; c.other_r=m_other_r;
      c.total_cost_points=c.entry_spread_points+c.exit_spread_points+c.entry_slippage_points+c.exit_slippage_points;
      c.total_cost_r=c.total_cost_points/r.initial_risk_points+c.commission_r+c.other_r;
      c.cost_hash=SF09_DeriveCostHash(c);
      error=""; return true;
   }
};

#endif
