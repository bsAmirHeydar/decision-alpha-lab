#property strict
#include <AlphaLab/StrategyFactory/Validation/SF12_AllValidation.mqh>
input string InpValidationPlanId="default_walk_forward";
input bool InpExportFoldLedger=true;
CSF12ValidationEngine g_validation;
int OnInit(){Print("SF12 research host initialized. Evidence-only: no paper/live order authority. plan=",InpValidationPlanId);return INIT_SUCCEEDED;}
void OnTick(){}
void OnDeinit(const int reason){const SF12_ValidationTelemetry t=g_validation.Telemetry();Print("SF12 telemetry accepted=",t.observations_accepted," rejected=",t.observations_rejected," gates_failed=",t.gates_failed);}
