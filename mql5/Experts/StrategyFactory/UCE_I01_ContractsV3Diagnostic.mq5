#property strict
#include <AlphaLab/StrategyFactory/Contracts/UCE03_AllContracts.mqh>
input bool InpRunOnTimer=true;
input int InpTimerSeconds=5;
UCE03_ContractTelemetry g_telemetry;

void EmitDiagnostic()
{
   CUCE03CanonicalObject dimensions;
   dimensions.AddLong("confirmation_time_ms",(long)TimeCurrent()*1000);
   dimensions.AddString("direction","neutral");
   dimensions.AddString("primary_symbol",_Symbol);
   dimensions.AddString("reference_symbol",_Symbol);
   dimensions.AddString("source_event_id","diagnostic");
   UCE03_IdentityKey key;
   key.kind=UCE03_ID_CONTEXT_OCCURRENCE;
   key.semantic_namespace="ucee.diagnostic";
   key.semantic_version="3.0.0";
   key.owner_id="strategy_factory";
   key.dimensions_json=dimensions.Serialize();
   g_telemetry.canonicalizations++;
   g_telemetry.identities_built++;
   Print("UCE-I01 | release=",UCE03_CONTRACT_RELEASE,
         " | identity=",UCE03_StableIdentity(key),
         " | canonical=",UCE03_IdentityCanonicalMaterial(key));
}
int OnInit()
{
   UCE03_ResetTelemetry(g_telemetry);
   if(InpRunOnTimer)EventSetTimer((int)MathMax(1,InpTimerSeconds));
   EmitDiagnostic();return INIT_SUCCEEDED;
}
void OnDeinit(const int reason){EventKillTimer();}
void OnTimer(){if(InpRunOnTimer)EmitDiagnostic();}
void OnTick(){}
