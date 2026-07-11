from __future__ import annotations
from .models import *
from .dataset import SourceObservation,build_dataset
from .enums import *
from .trainer import train_binary

def build_reference_training_bundle():
    columns=(FeatureColumn("reference.momentum","1.0.0",0,description="causal signed displacement").with_hash(),
             FeatureColumn("reference.volatility","1.0.0",1,description="causal normalized range").with_hash())
    label=LabelContract("reference_positive_net_r","1.0.0",LabelKind.BINARY_NET_R,positive_threshold_r=0.0).with_hash()
    observations=[]
    roles=(DatasetRole.TRAIN,)*12+(DatasetRole.VALIDATION,)*6+(DatasetRole.TEST,)*6
    for i,role in enumerate(roles):
        x=(i%6-2.5)/2.5;vol=0.2+(i%4)*0.1;net=0.6*x-0.1*vol
        observations.append(SourceObservation("fold_000",role,f"event_{i}",f"cluster_{i}",f"candidate_{i}",f"outcome_{i}",f"snapshot_{i}",
            1000+i*10,1001+i*10,1005+i*10,{"reference.momentum":x,"reference.volatility":vol},net))
    bundle=build_dataset(dataset_id="sf13_reference_dataset",dataset_version="1.0.0",strategy_id="reference_strategy",
        source_run_id="run_reference",source_manifest_hash="manifest_hash",source_artifact_hash="artifact_hash",
        validation_plan_hash="vplan_hash",columns=columns,label_contract=label,observations=observations,
        created_at_utc_msc=9999,code_revision="reference_revision")
    spec=TransformSpec()
    plan=TrainingPlan("sf13_reference_plan","1.0.0",TaskKind.BINARY_CLASSIFICATION,bundle.manifest.dataset_hash,
        bundle.manifest.feature_schema_hash,bundle.manifest.label_contract_hash,
        (ModelFamily.NEVER_TRADE,ModelFamily.ALWAYS_TRADE,ModelFamily.TRAIN_PREVALENCE,
         ModelFamily.SINGLE_FEATURE_THRESHOLD,ModelFamily.LOGISTIC_RIDGE,ModelFamily.DECISION_STUMP),
        spec.spec_hash,CalibrationMethod.PLATT,"log_loss",maximum_iterations=400).with_hash()
    trained=train_binary(bundle,label,plan,spec,generated_at_utc_msc=10000)
    return bundle,label,plan,trained
