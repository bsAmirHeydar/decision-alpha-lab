#ifndef __UCEI11_CATALOG_MQH__
#define __UCEI11_CATALOG_MQH__

#include "UCEI11_SearchDescriptor.mqh"

class CUCEI11Catalog
  {
private:
   static void Fill(UCEI11_SearchDescriptor &out,const string id,const UCEI11_SEARCH_KIND kind,
                    const bool native_adapter,const bool deterministic,const bool constraints,
                    const bool multi_objective,const bool pruning,const string dependency,
                    const string limitations)
     {
      out.adapter_id=id;
      out.adapter_version="1.0.0";
      out.kind=kind;
      out.native_adapter=native_adapter;
      out.deterministic=deterministic;
      out.supports_constraints=constraints;
      out.supports_multi_objective=multi_objective;
      out.supports_pruning=pruning;
      out.dependency_profile=dependency;
      out.limitations=limitations;
     }

public:
   static int Count()
     {
      return 10;
     }

   static bool Get(const int index,UCEI11_SearchDescriptor &out)
     {
      switch(index)
        {
         case 0: Fill(out,"uce.search.baseline",UCEI11_SEARCH_BASELINE,true,true,true,false,false,"",""); return true;
         case 1: Fill(out,"uce.search.grid",UCEI11_SEARCH_GRID,true,true,true,false,false,"",""); return true;
         case 2: Fill(out,"uce.search.random",UCEI11_SEARCH_RANDOM,true,true,true,false,false,"",""); return true;
         case 3: Fill(out,"uce.search.halton",UCEI11_SEARCH_QUASI_RANDOM,true,true,true,false,false,"",""); return true;
         case 4: Fill(out,"uce.search.tpe_reference",UCEI11_SEARCH_TPE,true,true,true,false,false,"","lightweight deterministic density ratio"); return true;
         case 5: Fill(out,"uce.search.successive_halving",UCEI11_SEARCH_SUCCESSIVE_HALVING,true,true,true,false,true,"",""); return true;
         case 6: Fill(out,"uce.search.hyperband",UCEI11_SEARCH_HYPERBAND,true,true,true,false,true,"",""); return true;
         case 7: Fill(out,"uce.search.evolutionary_reference",UCEI11_SEARCH_EVOLUTIONARY,true,true,true,false,false,"",""); return true;
         case 8: Fill(out,"uce.search.pareto",UCEI11_SEARCH_MULTI_OBJECTIVE,true,true,true,true,false,"",""); return true;
         case 9: Fill(out,"uce.search.optuna_tpe_adapter",UCEI11_SEARCH_TPE,false,false,true,true,true,"optuna>=4","pin dependency, sampler, storage, worker count"); return true;
        }
      return false;
     }
  };

#endif
