#ifndef __UCEI04_MATRIX_MQH__
#define __UCEI04_MATRIX_MQH__
#include "UCEI04_IntrabarPolicy.mqh"
class CUCEI04MatrixBudget{
public:
 bool Cardinality(const UCEI04_MatrixSpec &s,long &count,string &error){count=1;for(int i=0;i<ArraySize(s.axes);i++){int n=ArraySize(s.axes[i].values);if(n<=0){error="empty_matrix_axis";return false;}if(count>s.max_combinations/n){error="matrix_budget_exceeded";return false;}count*=n;}if(count>s.max_combinations){error="matrix_budget_exceeded";return false;}error="";return true;}
 void Seal(UCEI04_MatrixSpec &s){string m=s.matrix_id+"|"+s.version+"|"+UCEI03_SideName(s.side)+"|"+IntegerToString(s.max_combinations)+"|"+IntegerToString(s.max_compiled);for(int i=0;i<ArraySize(s.axes);i++)for(int j=0;j<ArraySize(s.axes[i].values);j++)m+="|"+s.axes[i].values[j].exact_key+"|"+s.axes[i].values[j].parameters.packet_id;s.definition_id="ucemx_"+UCE03_Fnv1a64HexUtf8(m);}
};
#endif
