#ifndef __DAL_ASTRO_FAMILY_THRESHOLDS_MQH__
#define __DAL_ASTRO_FAMILY_THRESHOLDS_MQH__

struct DAL_AstroThresholdProfile
{
   string family_name;
   string profile_name;
   double arm_threshold;
   double enter_threshold;
   double reduce_threshold;
   double exit_threshold;
   double natal_activation_minimum;
   double friction_minimum;
   double benefic_support_minimum;
   double malefic_pressure_minimum;
   double house_edge_minimum;
};

void DAL_AstroThresholdProfile_Reset(DAL_AstroThresholdProfile &p, const string family_name)
{
   p.family_name = family_name;
   p.profile_name = "baseline";
   p.arm_threshold = 58.0;
   p.enter_threshold = 66.0;
   p.reduce_threshold = 52.0;
   p.exit_threshold = 58.0;
   p.natal_activation_minimum = 40.0;
   p.friction_minimum = 60.0;
   p.benefic_support_minimum = 62.0;
   p.malefic_pressure_minimum = 60.0;
   p.house_edge_minimum = 8.0;
}

void DAL_AstroThresholdProfile_Load(const string family_name, DAL_AstroThresholdProfile &p)
{
   DAL_AstroThresholdProfile_Reset(p, family_name);

   if(family_name == "A0002_natal_resonance")
   {
      p.profile_name = "natal_resonance";
      p.arm_threshold = 60.0;
      p.enter_threshold = 67.0;
      p.reduce_threshold = 54.0;
      p.exit_threshold = 59.0;
      p.natal_activation_minimum = 46.0;
      return;
   }

   if(family_name == "A0003_friction_polarity")
   {
      p.profile_name = "friction_guard";
      p.arm_threshold = 57.0;
      p.enter_threshold = 65.0;
      p.reduce_threshold = 50.0;
      p.exit_threshold = 57.0;
      p.friction_minimum = 58.0;
      return;
   }

   if(family_name == "A0090_live_shell")
   {
      p.profile_name = "validated_live_shell";
      p.arm_threshold = 60.0;
      p.enter_threshold = 68.0;
      p.reduce_threshold = 54.0;
      p.exit_threshold = 60.0;
      return;
   }

   if(family_name == "A0004_sect_benefic_pressure")
   {
      p.profile_name = "sect_benefic_pressure";
      p.arm_threshold = 59.0;
      p.enter_threshold = 67.0;
      p.reduce_threshold = 53.0;
      p.exit_threshold = 59.0;
      p.benefic_support_minimum = 64.0;
      p.malefic_pressure_minimum = 62.0;
      p.house_edge_minimum = 10.0;
      return;
   }

   if(family_name == "A0001_transit_trend_pulse")
      p.profile_name = "baseline";
}

#endif
