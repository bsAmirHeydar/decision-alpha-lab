#ifndef __DAL_ASTRO_DOCTRINE_CONTEXT_MQH__
#define __DAL_ASTRO_DOCTRINE_CONTEXT_MQH__

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroDerivedFeatures.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>

struct DAL_AstroDoctrineContext
{
   bool   valid;
   bool   diurnal_sect;
   string sect_name;
   double benefic_support_score;
   double malefic_pressure_score;
   double angular_power_score;
   double house_lift_score;
   double house_drag_score;
   double rulership_chain_score;
   double reception_score;
   string context_key;
};

void DAL_AstroDC_Reset(DAL_AstroDoctrineContext &d)
{
   d.valid = false;
   d.diurnal_sect = true;
   d.sect_name = "day";
   d.benefic_support_score = 0.0;
   d.malefic_pressure_score = 0.0;
   d.angular_power_score = 0.0;
   d.house_lift_score = 0.0;
   d.house_drag_score = 0.0;
   d.rulership_chain_score = 0.0;
   d.reception_score = 0.0;
   d.context_key = "";
}

double DAL_AstroDC_HousePower(const int house)
{
   if(house == 1 || house == 10 || house == 7 || house == 4) return 100.0;
   if(house == 2 || house == 11 || house == 8 || house == 5) return 66.0;
   if(house == 3 || house == 9) return 54.0;
   if(house == 6 || house == 12) return 34.0;
   return 40.0;
}

double DAL_AstroDC_HouseLift(const int house)
{
   if(house == 10) return 100.0;
   if(house == 1 || house == 11) return 92.0;
   if(house == 5 || house == 9) return 78.0;
   if(house == 2 || house == 7) return 62.0;
   if(house == 3 || house == 4) return 46.0;
   if(house == 6 || house == 8) return 26.0;
   if(house == 12) return 18.0;
   return 40.0;
}

double DAL_AstroDC_HouseDrag(const int house)
{
   if(house == 12) return 100.0;
   if(house == 8 || house == 6) return 84.0;
   if(house == 4) return 70.0;
   if(house == 3) return 52.0;
   if(house == 7 || house == 2) return 40.0;
   if(house == 9 || house == 5) return 28.0;
   if(house == 11 || house == 1) return 18.0;
   if(house == 10) return 12.0;
   return 40.0;
}

double DAL_AstroDC_DignityScore(const DAL_AstroBodyState &b)
{
   if(b.dignity_score > 0.0)
      return b.dignity_score;

   string sign = b.sign;
   string name = b.name;

   if(name == "sun")
   {
      if(sign == "leo") return 95.0;
      if(sign == "aries") return 86.0;
      if(sign == "aquarius") return 18.0;
      if(sign == "libra") return 10.0;
   }
   if(name == "moon")
   {
      if(sign == "cancer") return 95.0;
      if(sign == "taurus") return 86.0;
      if(sign == "capricorn") return 18.0;
      if(sign == "scorpio") return 10.0;
   }
   if(name == "mercury")
   {
      if(sign == "gemini" || sign == "virgo") return 92.0;
      if(sign == "virgo") return 96.0;
      if(sign == "sagittarius" || sign == "pisces") return 18.0;
      if(sign == "pisces") return 10.0;
   }
   if(name == "venus")
   {
      if(sign == "taurus" || sign == "libra") return 92.0;
      if(sign == "pisces") return 96.0;
      if(sign == "scorpio" || sign == "aries") return 18.0;
      if(sign == "virgo") return 10.0;
   }
   if(name == "mars")
   {
      if(sign == "aries" || sign == "scorpio") return 92.0;
      if(sign == "capricorn") return 96.0;
      if(sign == "libra" || sign == "taurus") return 18.0;
      if(sign == "cancer") return 10.0;
   }
   if(name == "jupiter")
   {
      if(sign == "sagittarius" || sign == "pisces") return 92.0;
      if(sign == "cancer") return 96.0;
      if(sign == "gemini" || sign == "virgo") return 18.0;
      if(sign == "capricorn") return 10.0;
   }
   if(name == "saturn")
   {
      if(sign == "capricorn" || sign == "aquarius") return 92.0;
      if(sign == "libra") return 96.0;
      if(sign == "cancer" || sign == "leo") return 18.0;
      if(sign == "aries") return 10.0;
   }

   return 50.0;
}

double DAL_AstroDC_SectFavorability(const DAL_AstroBodyState &b, const bool diurnal)
{
   if(b.name == "sun")
      return diurnal ? 96.0 : 34.0;
   if(b.name == "moon")
      return diurnal ? 38.0 : 96.0;
   if(b.name == "jupiter")
      return diurnal ? 92.0 : 60.0;
   if(b.name == "venus")
      return diurnal ? 62.0 : 92.0;
   if(b.name == "saturn")
      return diurnal ? 78.0 : 28.0;
   if(b.name == "mars")
      return diurnal ? 28.0 : 76.0;
   if(b.name == "mercury")
      return 64.0;
   return 50.0;
}

double DAL_AstroDC_TriplicityScore(const DAL_AstroBodyState &b)
{
   if(b.triplicity_score > 0.0)
      return b.triplicity_score;
   return 18.0;
}

double DAL_AstroDC_SolarConditionScore(const DAL_AstroBodyState &b)
{
   if(b.solar_condition == "cazimi") return 98.0;
   if(b.solar_condition == "free" || b.solar_condition == "n/a") return 72.0;
   if(b.solar_condition == "under_beams") return 42.0;
   if(b.solar_condition == "combust") return 15.0;
   return 50.0;
}

bool DAL_AstroDC_Calc(const DAL_AstroMapRow &row, DAL_AstroDoctrineContext &d)
{
   DAL_AstroDC_Reset(d);

   int idx_sun = DAL_AstroBodyIndexByName("sun");
   int idx_moon = DAL_AstroBodyIndexByName("moon");
   int idx_mercury = DAL_AstroBodyIndexByName("mercury");
   int idx_venus = DAL_AstroBodyIndexByName("venus");
   int idx_mars = DAL_AstroBodyIndexByName("mars");
   int idx_jupiter = DAL_AstroBodyIndexByName("jupiter");
   int idx_saturn = DAL_AstroBodyIndexByName("saturn");
   if(idx_sun < 0 || idx_moon < 0 || idx_mercury < 0 || idx_venus < 0 || idx_mars < 0 || idx_jupiter < 0 || idx_saturn < 0)
      return false;

   DAL_AstroBodyState sun = row.body[idx_sun];
   DAL_AstroBodyState moon = row.body[idx_moon];
   DAL_AstroBodyState mercury = row.body[idx_mercury];
   DAL_AstroBodyState venus = row.body[idx_venus];
   DAL_AstroBodyState mars = row.body[idx_mars];
   DAL_AstroBodyState jupiter = row.body[idx_jupiter];
   DAL_AstroBodyState saturn = row.body[idx_saturn];

   d.diurnal_sect = (sun.house >= 7 && sun.house <= 12);
   d.sect_name = d.diurnal_sect ? "day" : "night";

   double venus_help = 0.34 * DAL_AstroDC_DignityScore(venus) + 0.22 * DAL_AstroDC_HouseLift(venus.house) + 0.14 * DAL_AstroDC_SectFavorability(venus, d.diurnal_sect) + 0.10 * DAL_AstroDC_TriplicityScore(venus) + 0.10 * DAL_AstroDC_SolarConditionScore(venus) + 0.10 * (venus.retro == 1 ? 30.0 : 72.0);
   double jupiter_help = 0.34 * DAL_AstroDC_DignityScore(jupiter) + 0.22 * DAL_AstroDC_HouseLift(jupiter.house) + 0.14 * DAL_AstroDC_SectFavorability(jupiter, d.diurnal_sect) + 0.10 * DAL_AstroDC_TriplicityScore(jupiter) + 0.10 * DAL_AstroDC_SolarConditionScore(jupiter) + 0.10 * (jupiter.retro == 1 ? 38.0 : 70.0);
   d.benefic_support_score = DAL_AstroPM_Clamp((venus_help + jupiter_help) / 2.0);

   double mars_push = 0.36 * DAL_AstroDC_DignityScore(mars) + 0.20 * DAL_AstroDC_HouseDrag(mars.house) + 0.18 * (100.0 - DAL_AstroDC_SectFavorability(mars, d.diurnal_sect)) + 0.10 * DAL_AstroDC_TriplicityScore(mars) + 0.08 * (100.0 - DAL_AstroDC_SolarConditionScore(mars)) + 0.08 * row.nodal_pressure_score + 0.12 * (mars.retro == 1 ? 56.0 : 72.0);
   double saturn_push = 0.36 * DAL_AstroDC_DignityScore(saturn) + 0.20 * DAL_AstroDC_HouseDrag(saturn.house) + 0.18 * (100.0 - DAL_AstroDC_SectFavorability(saturn, d.diurnal_sect)) + 0.10 * DAL_AstroDC_TriplicityScore(saturn) + 0.08 * (100.0 - DAL_AstroDC_SolarConditionScore(saturn)) + 0.08 * row.nodal_pressure_score + 0.12 * (saturn.retro == 1 ? 46.0 : 68.0);
   d.malefic_pressure_score = DAL_AstroPM_Clamp((mars_push + saturn_push) / 2.0);

   d.angular_power_score = DAL_AstroPM_Clamp(
      0.22 * DAL_AstroDC_HousePower(sun.house) +
      0.18 * DAL_AstroDC_HousePower(moon.house) +
      0.15 * DAL_AstroDC_HousePower(venus.house) +
      0.15 * DAL_AstroDC_HousePower(mars.house) +
      0.15 * DAL_AstroDC_HousePower(jupiter.house) +
      0.15 * DAL_AstroDC_HousePower(saturn.house)
   );

   d.house_lift_score = DAL_AstroPM_Clamp(
      0.25 * DAL_AstroDC_HouseLift(sun.house) +
      0.15 * DAL_AstroDC_HouseLift(moon.house) +
      0.10 * DAL_AstroDC_HouseLift(mercury.house) +
      0.10 * DAL_AstroDC_HouseLift(venus.house) +
      0.15 * DAL_AstroDC_HouseLift(mars.house) +
      0.15 * DAL_AstroDC_HouseLift(jupiter.house) +
      0.10 * DAL_AstroDC_HouseLift(saturn.house)
   );

   d.house_drag_score = DAL_AstroPM_Clamp(
      0.20 * DAL_AstroDC_HouseDrag(sun.house) +
      0.18 * DAL_AstroDC_HouseDrag(moon.house) +
      0.10 * DAL_AstroDC_HouseDrag(venus.house) +
      0.16 * DAL_AstroDC_HouseDrag(mars.house) +
      0.12 * DAL_AstroDC_HouseDrag(jupiter.house) +
      0.24 * DAL_AstroDC_HouseDrag(saturn.house)
   );
   d.rulership_chain_score = row.rulership_chain_score;
   d.reception_score = DAL_AstroPM_Clamp(18.0 * row.mutual_reception_count);

   d.context_key =
      "sect=" + d.sect_name +
      "|benefic=" + DAL_AstroPM_Bucket5(d.benefic_support_score) +
      "|malefic=" + DAL_AstroPM_Bucket5(d.malefic_pressure_score) +
      "|angular=" + DAL_AstroPM_Bucket5(d.angular_power_score) +
      "|lift=" + DAL_AstroPM_Bucket5(d.house_lift_score) +
      "|drag=" + DAL_AstroPM_Bucket5(d.house_drag_score) +
      "|chain=" + DAL_AstroPM_Bucket5(d.rulership_chain_score) +
      "|reception=" + DAL_AstroPM_Bucket5(d.reception_score);

   d.valid = true;
   return true;
}

#endif
