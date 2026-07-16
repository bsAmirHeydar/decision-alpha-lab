#pragma once
bool SAEDV418OverlapSupported(const double p,const double floor_value){ return MathIsValidNumber(p) && p>=floor_value && p<=1.0-floor_value; }
int SAEDV418UnsupportedDirective(){ return V418_SKIP; }
