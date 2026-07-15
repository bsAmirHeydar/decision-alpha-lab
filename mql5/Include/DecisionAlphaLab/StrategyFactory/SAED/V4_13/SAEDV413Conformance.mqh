#pragma once
bool SAEDV413WithinTolerance(const double a,const double b,const double tolerance){ return MathAbs(a-b)<=tolerance; }
