#property strict
#include <AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph/GraphAll.mqh>

int OnInit()
  {
   SAEDHypergraphAuthorityBoundary authority;
   SAEDHypergraphDefaultAuthority(authority);
   if(!SAEDHypergraphAuthorityValid(authority))
      return INIT_FAILED;
   authority.train_model=true;
   if(SAEDHypergraphAuthorityValid(authority))
      return INIT_FAILED;
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
  }
