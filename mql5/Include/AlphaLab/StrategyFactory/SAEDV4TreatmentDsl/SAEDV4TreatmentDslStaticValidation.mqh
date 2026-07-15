#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_STATIC_VALIDATION_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_STATIC_VALIDATION_MQH

bool SAEDV4DslContainsProhibitedToken(const string value)
  {
   string lowered=value;
   StringToLower(lowered);
   const string forbidden[8]={"future","outcome","realized_pnl","forward_return","lot_size","leverage","capital_allocation","position_size"};
   for(int i=0;i<ArraySize(forbidden);i++)
      if(StringFind(lowered,forbidden[i])>=0) return true;
   return false;
  }

bool SAEDV4DslBudgetValid(const int components,const int parameters,const int constraints,const int states,const int transitions)
  {
   return(components>=1 && components<=16 && parameters>=0 && parameters<=128 && constraints>=0 && constraints<=64 && states>=0 && states<=32 && transitions>=0 && transitions<=64);
  }
#endif
