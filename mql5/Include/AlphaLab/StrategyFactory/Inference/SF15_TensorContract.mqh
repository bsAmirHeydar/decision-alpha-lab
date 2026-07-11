#ifndef __SF15_TENSOR_CONTRACT_MQH__
#define __SF15_TENSOR_CONTRACT_MQH__
#include "SF15_Hashing.mqh"
struct SF15_TensorContract
  {
   string name; int element_type; int ordinal; ulong shape[]; string contract_hash;
   void Reset(){name="";element_type=1;ordinal=0;ArrayResize(shape,0);contract_hash="";}
   string Canonical() const
     {
      string dims=""; for(int i=0;i<ArraySize(shape);i++){if(i>0)dims+=",";dims+=IntegerToString((long)shape[i]);}
      return "alpha_lab.strategy_factory/tensor_contract@1.0.0|"+name+"|"+IntegerToString(element_type)+"|"+IntegerToString(ordinal)+"|"+dims;
     }
   bool Validate(string &error) const
     {
      if(name=="" || element_type!=1 || ordinal<0 || ArraySize(shape)<1){error="invalid tensor identity";return false;}
      for(int i=0;i<ArraySize(shape);i++)if(shape[i]<1){error="invalid tensor shape";return false;}
      error="";return true;
     }
  };
#endif
