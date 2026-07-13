#ifndef __EXP0019_FP_I04_SYMBOL_PAIR_MQH__
#define __EXP0019_FP_I04_SYMBOL_PAIR_MQH__
#include "FP_I04_Types.mqh"
#include <FaerieProtocol/EXP0019/Core/FP_I02_All.mqh>
void FP_I04_DefaultSymbol(FP_I04_SymbolSpec &s,const string canonical,const string aliases,const double tick_size,const int digits)
  { s.canonical_symbol=canonical;s.aliases_csv=aliases;s.tick_size=tick_size;s.digits=digits;s.spec_hash=FP_I02_CompactId("FPSYM",canonical+"|"+aliases+"|"+DoubleToString(tick_size,8)+"|"+IntegerToString(digits)); }
void FP_I04_DefaultPair(FP_I04_SymbolPair &p)
  { p.context_id="FP-CONTEXT-001";p.pair_id="FP-PAIR-ES-NQ";FP_I04_DefaultSymbol(p.left,"ES","ES,US500",0.25,2);FP_I04_DefaultSymbol(p.right,"NQ","NQ,USTEC",0.25,2);p.pair_hash=FP_I02_CompactId("FPPAIR",p.context_id+"|"+p.pair_id+"|"+p.left.spec_hash+"|"+p.right.spec_hash); }
bool FP_I04_ResolveSymbol(const FP_I04_SymbolPair &p,const string raw,string &canonical)
  { string key=raw;StringToUpper(key);string aliases[];int count=StringSplit(p.left.aliases_csv,StringGetCharacter(",",0),aliases);for(int i=0;i<count;i++){string a=aliases[i];StringToUpper(a);if(key==a){canonical=p.left.canonical_symbol;return true;}}count=StringSplit(p.right.aliases_csv,StringGetCharacter(",",0),aliases);for(int i=0;i<count;i++){string a=aliases[i];StringToUpper(a);if(key==a){canonical=p.right.canonical_symbol;return true;}}canonical="";return false; }
#endif
