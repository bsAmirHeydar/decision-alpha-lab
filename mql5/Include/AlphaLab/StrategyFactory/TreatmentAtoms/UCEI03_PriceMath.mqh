#ifndef __UCEI03_PRICE_MATH_MQH__
#define __UCEI03_PRICE_MATH_MQH__
#include "UCEI03_ParameterPacket.mqh"
double UCEI03_EntryExecutable(const UCEI03_PriceEnvironment &p,const ENUM_UCEI03_SIDE side){return side==UCEI03_LONG?p.ask:p.bid;}
double UCEI03_ExitExecutable(const UCEI03_PriceEnvironment &p,const ENUM_UCEI03_SIDE side){return side==UCEI03_LONG?p.bid:p.ask;}
double UCEI03_RoundNearestTick(const UCEI03_PriceEnvironment &p,const double price){return NormalizeDouble(MathRound(price/p.tick_size)*p.tick_size,p.digits);}
double UCEI03_RoundFloorTick(const UCEI03_PriceEnvironment &p,const double price){return NormalizeDouble(MathFloor((price+1e-12)/p.tick_size)*p.tick_size,p.digits);}
double UCEI03_RoundCeilTick(const UCEI03_PriceEnvironment &p,const double price){return NormalizeDouble(MathCeil((price-1e-12)/p.tick_size)*p.tick_size,p.digits);}
double UCEI03_ConservativePrice(const UCEI03_PriceEnvironment &p,const ENUM_UCEI03_SIDE side,const ENUM_UCEI03_PRICE_ROLE role,const double price){if(role==UCEI03_PRICE_STOP||role==UCEI03_PRICE_TRAIL)return side==UCEI03_LONG?UCEI03_RoundCeilTick(p,price):UCEI03_RoundFloorTick(p,price);if(role==UCEI03_PRICE_TARGET)return side==UCEI03_LONG?UCEI03_RoundFloorTick(p,price):UCEI03_RoundCeilTick(p,price);return UCEI03_RoundNearestTick(p,price);}
bool UCEI03_ValidateProtectiveStop(const UCEI03_BuildContext &c,const double stop,string &error){double entry=UCEI03_EntryExecutable(c.price,c.side);if((c.side==UCEI03_LONG&&stop>=entry)||(c.side==UCEI03_SHORT&&stop<=entry)){error="stop is not protective";return false;}error="";return true;}
bool UCEI03_ValidateFavorableTarget(const UCEI03_BuildContext &c,const double target,string &error){double entry=UCEI03_EntryExecutable(c.price,c.side);if((c.side==UCEI03_LONG&&target<=entry)||(c.side==UCEI03_SHORT&&target>=entry)){error="target is not favorable";return false;}error="";return true;}
bool UCEI03_ValidatePending(const UCEI03_BuildContext &c,const ENUM_UCEI03_ORDER_TYPE type,const double price,string &error){double min_distance=c.price.stops_level_points*c.price.point;if(type==UCEI03_ORDER_LIMIT){if((c.side==UCEI03_LONG&&price>c.price.ask-min_distance)||(c.side==UCEI03_SHORT&&price<c.price.bid+min_distance)){error="limit violates executable-side distance";return false;}}if(type==UCEI03_ORDER_STOP){if((c.side==UCEI03_LONG&&price<c.price.ask+min_distance)||(c.side==UCEI03_SHORT&&price>c.price.bid-min_distance)){error="stop trigger violates executable-side distance";return false;}}error="";return true;}
#endif
