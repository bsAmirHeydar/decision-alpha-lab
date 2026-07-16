#pragma once
double SAEDV418LowerBound(const double value,const double standard_error,const double z_score){ return value-z_score*MathMax(0.0,standard_error); }
