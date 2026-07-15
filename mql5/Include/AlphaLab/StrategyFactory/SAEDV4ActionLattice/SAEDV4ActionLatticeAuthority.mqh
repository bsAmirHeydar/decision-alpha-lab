#ifndef __ALPHALAB_SAEDV4ACTIONLATTICEAUTHORITY_MQH__
#define __ALPHALAB_SAEDV4ACTIONLATTICEAUTHORITY_MQH__

// SAED V4-07 diagnostic-only mirror. No trading, file, socket or network authority.
bool SAEDV407HasExecutionAuthority(){ return false; }
bool SAEDV407HasSelectionAuthority(){ return false; }
bool SAEDV407MayBuildBoundedLattice(){ return true; }

#endif // __ALPHALAB_SAEDV4ACTIONLATTICEAUTHORITY_MQH__
