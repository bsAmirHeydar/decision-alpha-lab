#ifndef ALPHALAB_UCEI13_REGISTRY
#define ALPHALAB_UCEI13_REGISTRY
#include "UCEI13_Catalog.mqh"
bool UCEI13RegistryValid(){if(UCEI13CatalogCount()!=14)return false;for(int i=0;i<UCEI13CatalogCount();i++){UCEI13NodeDescriptor d;if(!UCEI13CatalogAt(i,d)||d.runtime_authority)return false;}return true;}
#endif
