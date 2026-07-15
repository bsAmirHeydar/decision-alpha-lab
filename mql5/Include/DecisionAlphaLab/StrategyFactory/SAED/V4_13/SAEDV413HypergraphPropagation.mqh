#pragma once
double SAEDV413BoundedTanh(const double x){ return MathTanh(MathMax(-30.0,MathMin(30.0,x))); }
