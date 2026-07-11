#ifndef __SF09_PRICE_OBSERVATION_MQH__
#define __SF09_PRICE_OBSERVATION_MQH__
#include "../Contracts/SF01_AllContracts.mqh"
#include "SF09_OutcomeEnums.mqh"

struct SF09_PriceObservation
{
   string observation_id;
   string symbol;
   ENUM_SF09_OBSERVATION_KIND kind;
   ENUM_SF09_DATA_FIDELITY fidelity;
   long sequence;
   SF01_MarketTimestamp observed_at;
   SF01_MarketTimestamp interval_open;
   SF01_MarketTimestamp interval_close;
   double open_price;
   double high_price;
   double low_price;
   double close_price;
   bool has_bid_ask;
   double bid_price;
   double ask_price;
   double spread_points;
   string source_hash;
};

string SF09_PriceObservationCanonical(const SF09_PriceObservation &o)
{
   return o.symbol+"|"+IntegerToString((int)o.kind)+"|"+IntegerToString((int)o.fidelity)+"|"+
          IntegerToString(o.sequence)+"|"+IntegerToString(o.observed_at.utc_epoch_milliseconds)+"|"+
          IntegerToString(o.interval_open.utc_epoch_milliseconds)+"|"+IntegerToString(o.interval_close.utc_epoch_milliseconds)+"|"+
          SF01_CanonicalDouble(o.open_price)+"|"+SF01_CanonicalDouble(o.high_price)+"|"+
          SF01_CanonicalDouble(o.low_price)+"|"+SF01_CanonicalDouble(o.close_price)+"|"+
          SF01_CanonicalBool(o.has_bid_ask)+"|"+SF01_CanonicalDouble(o.bid_price)+"|"+
          SF01_CanonicalDouble(o.ask_price)+"|"+SF01_CanonicalDouble(o.spread_points)+"|"+o.source_hash;
}

string SF09_DerivePriceObservationId(const SF09_PriceObservation &o)
{return SF01_StableId("pobs",SF09_PriceObservationCanonical(o));}

bool SF09_ValidatePriceObservation(const SF09_PriceObservation &o,string &error)
{
   if(!SF01_IsTerminalSymbol(o.symbol) || !SF01_IsSafeIdentifier(o.source_hash,128))
   { error="invalid observation identity"; return false; }
   if(o.kind!=SF09_OBSERVATION_TICK && o.kind!=SF09_OBSERVATION_CLOSED_BAR)
   { error="invalid observation kind"; return false; }
   if(o.fidelity<SF09_FIDELITY_BAR_APPROXIMATION || o.fidelity>SF09_FIDELITY_REAL_TICK)
   { error="invalid data fidelity"; return false; }
   if(o.sequence<0 || !SF01_ValidateTimestamp(o.observed_at,error) ||
      !SF01_ValidateTimestamp(o.interval_open,error) || !SF01_ValidateTimestamp(o.interval_close,error)) return false;
   if(o.interval_close.utc_epoch_milliseconds<o.interval_open.utc_epoch_milliseconds)
   { error="observation interval is reversed"; return false; }
   if(o.observed_at.utc_epoch_milliseconds<o.interval_close.utc_epoch_milliseconds)
   { error="observation known before interval close"; return false; }
   if(!MathIsValidNumber(o.open_price)||!MathIsValidNumber(o.high_price)||!MathIsValidNumber(o.low_price)||!MathIsValidNumber(o.close_price))
   { error="non-finite observation price"; return false; }
   if(o.low_price<=0.0 || o.high_price<o.low_price || o.open_price<o.low_price || o.open_price>o.high_price || o.close_price<o.low_price || o.close_price>o.high_price)
   { error="invalid observation geometry"; return false; }
   if(o.has_bid_ask)
   {
      if(!MathIsValidNumber(o.bid_price)||!MathIsValidNumber(o.ask_price)||o.bid_price<=0.0||o.ask_price<o.bid_price)
      { error="invalid bid ask geometry"; return false; }
   }
   if(!MathIsValidNumber(o.spread_points)||o.spread_points<0.0)
   { error="invalid spread points"; return false; }
   const string expected=SF09_DerivePriceObservationId(o);
   if(o.observation_id!="" && o.observation_id!=expected)
   { error="observation id mismatch"; return false; }
   error=""; return true;
}

#endif
