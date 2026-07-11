#ifndef __SF13_TRAINING_TELEMETRY_MQH__
#define __SF13_TRAINING_TELEMETRY_MQH__
#include "SF13_DatasetExporter.mqh"
struct SF13_TrainingTelemetry{long rows_observed;long rows_rejected;long duplicate_rows;long cluster_role_violations;long manifests_emitted;long prediction_contract_failures;};
void SF13_ResetTelemetry(SF13_TrainingTelemetry &v){v.rows_observed=0;v.rows_rejected=0;v.duplicate_rows=0;v.cluster_role_violations=0;v.manifests_emitted=0;v.prediction_contract_failures=0;}
#endif
