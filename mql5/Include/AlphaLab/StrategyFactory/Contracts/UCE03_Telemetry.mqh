#ifndef __UCE03_TELEMETRY_MQH__
#define __UCE03_TELEMETRY_MQH__
struct UCE03_ContractTelemetry
{
   long canonicalizations;
   long identities_built;
   long schema_resolutions;
   long migrations_applied;
   long compatibility_accepts;
   long compatibility_rejections;
   long causal_rejections;
   long legacy_bridges;
};
void UCE03_ResetTelemetry(UCE03_ContractTelemetry &value)
{
   value.canonicalizations=0;value.identities_built=0;value.schema_resolutions=0;value.migrations_applied=0;
   value.compatibility_accepts=0;value.compatibility_rejections=0;value.causal_rejections=0;value.legacy_bridges=0;
}
#endif
