#ifndef ALPHALAB_UCEI14_GENERATION
#define ALPHALAB_UCEI14_GENERATION
#include "UCEI14_Contracts.mqh"
bool UCEI14CanWarm(const UCEI14Generation &g){return(g.state==UCEI14_BUILT);}
bool UCEI14CanValidate(const UCEI14Generation &g,const bool parity_pass){return(g.state==UCEI14_WARMED&&parity_pass);}
bool UCEI14CanActivate(const UCEI14Generation &g,const UCEI14BundleManifest &m){return(g.state==UCEI14_VALIDATED&&m.signature_valid&&m.parity_pass&&g.bundle_hash==m.bundle_hash);}
void UCEI14Retire(UCEI14Generation &g){g.state=UCEI14_RETIRED;}
#endif
