#ifndef SAEDV422_STRESS_COMPOSER_MQH
#define SAEDV422_STRESS_COMPOSER_MQH
double SAEDV422GapFactor(const bool down,const double severity){return down?(1.0-0.08*severity):(1.0+0.08*severity);}
double SAEDV422LiquidityStress(const double liquidity,const double severity){return MathMax(0.0,MathMin(1.0,liquidity*(1.0-0.85*severity)));}
#endif
