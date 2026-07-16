#pragma once
enum SAEDV418Treatment { V418_SKIP=0, V418_MANUAL=1, V418_ADAPTIVE_A=2, V418_ADAPTIVE_B=3 };
int SAEDV418TreatmentCount(){ return 4; }
bool SAEDV418TreatmentUniverseFrozen(){ return true; }
