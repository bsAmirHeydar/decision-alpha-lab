#ifndef ALPHALAB_UCEI13_FALLBACK
#define ALPHALAB_UCEI13_FALLBACK
#include "UCEI13_Contracts.mqh"
UCEI13Fallback UCEI13FallbackFor(const bool risk_rejected,const bool conflict){if(risk_rejected)return UCEI13_REJECT;if(conflict)return UCEI13_ABSTAIN;return UCEI13_MANUAL_ONLY;}
#endif
