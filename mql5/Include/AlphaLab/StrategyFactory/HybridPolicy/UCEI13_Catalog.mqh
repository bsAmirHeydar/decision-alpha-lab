#ifndef ALPHALAB_UCEI13_CATALOG
#define ALPHALAB_UCEI13_CATALOG
#include "UCEI13_NodeDescriptor.mqh"
int UCEI13CatalogCount(){return 14;}
bool UCEI13CatalogAt(const int i,UCEI13NodeDescriptor &d){switch(i){case 0:d.key="input";break;case 1:d.key="manual_eligibility";break;case 2:d.key="manual_treatment";break;case 3:d.key="model_filter";break;case 4:d.key="model_rank";break;case 5:d.key="model_treatment";break;case 6:d.key="model_risk";break;case 7:d.key="manual_veto";break;case 8:d.key="operator_approval";break;case 9:d.key="portfolio_allocation";break;case 10:d.key="risk_gate";break;case 11:d.key="kill_switch";break;case 12:d.key="fallback";break;case 13:d.key="output";break;default:return false;}d.deterministic=true;d.runtime_authority=false;return true;}
#endif
