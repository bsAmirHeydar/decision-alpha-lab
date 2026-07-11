from __future__ import annotations
from dataclasses import dataclass
from .enums import *
from .models import *
from .dataset import DatasetBundle, rows_for_role
from .transforms import fit_transform_state, apply_transform
from .registry import StaticTrainerRegistry, reference_registry
from .calibration import fit_calibration, apply_calibration
from .metrics import score_binary, regression_metrics
from .hashing import sha256_lines, stable_id

@dataclass(frozen=True,slots=True)
class CandidateEvaluation:
    family:ModelFamily
    validation_score:float
    validation_metrics:dict[str,float]
    model:object

@dataclass(frozen=True,slots=True)
class TrainingBundle:
    transform:TransformState
    model:ModelArtifact
    calibration:CalibrationArtifact
    predictions:tuple[PredictionRecord,...]
    card:ModelCard
    report:TrainingReportManifest
    candidate_evaluations:tuple[CandidateEvaluation,...]

def _metric_value(metric:str,metrics:dict[str,float])->float:
    if metric not in metrics:raise ValueError(f"unknown selection metric: {metric}")
    value=metrics[metric]
    return -value if metric in {"log_loss","brier","ece","mae","rmse"} else value

def train_binary(bundle:DatasetBundle,label_contract:LabelContract,plan:TrainingPlan,
                 transform_spec:TransformSpec,registry:StaticTrainerRegistry|None=None,
                 generated_at_utc_msc:int=0)->TrainingBundle:
    plan.validate();bundle.manifest.validate();label_contract.validate()
    if plan.task!=TaskKind.BINARY_CLASSIFICATION or label_contract.kind!=LabelKind.BINARY_NET_R:
        raise ValueError("binary trainer requires binary task and label contract")
    if plan.dataset_hash!=bundle.manifest.dataset_hash or plan.feature_schema_hash!=bundle.manifest.feature_schema_hash or plan.label_contract_hash!=bundle.manifest.label_contract_hash:
        raise ValueError("training-plan lineage mismatch")
    train_rows=rows_for_role(bundle.rows,DatasetRole.TRAIN);validation_rows=rows_for_role(bundle.rows,DatasetRole.VALIDATION);test_rows=rows_for_role(bundle.rows,DatasetRole.TEST)
    transform=fit_transform_state(train_rows,bundle.columns,bundle.manifest.feature_schema_hash,transform_spec)
    x_train=[apply_transform(row,transform,transform_spec) for row in train_rows];y_train=[float(row.label_value) for row in train_rows]
    x_val=[apply_transform(row,transform,transform_spec) for row in validation_rows];y_val=[float(row.label_value) for row in validation_rows]
    registry=registry or reference_registry();evaluations=[]
    for family in plan.model_families:
        plugin=registry.resolve(family,"1.0.0",plan.task);fitted=plugin.fit(x_train,y_train,plan)
        probabilities=[fitted.probability(row) for row in x_val];metrics=score_binary(y_val,probabilities)
        evaluations.append(CandidateEvaluation(family,_metric_value(plan.selection_metric,metrics),metrics,fitted))
    evaluations.sort(key=lambda e:(-e.validation_score,int(e.family)))
    selected=evaluations[0]
    model=ModelArtifact(model_id=f"sf13.{selected.family.name.lower()}",model_version="1.0.0",family=selected.family,
        task=plan.task,training_plan_hash=plan.plan_hash,dataset_hash=bundle.manifest.dataset_hash,
        feature_schema_hash=bundle.manifest.feature_schema_hash,label_contract_hash=bundle.manifest.label_contract_hash,
        transform_hash=transform.transform_hash,training_rowset_hash=transform.fitted_rowset_hash,
        parameter_names=selected.model.parameter_names,parameter_values=selected.model.parameter_values,
        selected_on_role=DatasetRole.VALIDATION,random_seed=plan.random_seed).with_hash();model.validate()
    raw_val=[selected.model.raw(row) for row in x_val]
    calibration=fit_calibration(plan.calibration_method,raw_val,y_val,model.artifact_hash,
        [row.row_hash for row in validation_rows])
    x_test=[apply_transform(row,transform,transform_spec) for row in test_rows];y_test=[float(row.label_value) for row in test_rows]
    predictions=[]
    for row,features in zip(test_rows,x_test):
        raw=selected.model.raw(features);probability=apply_calibration(raw,calibration)
        prediction=PredictionRecord(model_artifact_hash=model.artifact_hash,calibration_hash=calibration.calibration_hash,
            dataset_hash=bundle.manifest.dataset_hash,row_id=row.row_id,fold_id=row.fold_id,role=PredictionRole.TEST_OOS,
            raw_score=raw,probability=probability,action_score=probability-0.5,
            generated_at_utc_msc=generated_at_utc_msc).with_hashes();prediction.validate();predictions.append(prediction)
    test_metrics=score_binary(y_test,[p.probability for p in predictions])
    card=ModelCard(model_artifact_hash=model.artifact_hash,training_plan_hash=plan.plan_hash,
        dataset_hash=bundle.manifest.dataset_hash,selection_metric=plan.selection_metric,
        validation_score=selected.validation_metrics[plan.selection_metric],test_score=test_metrics[plan.selection_metric],
        test_sample_count=len(test_rows),calibration_hash=calibration.calibration_hash,
        intended_use="offline research comparison and Phase 14 registry review only",
        limitations=("reference baseline family","single frozen dataset manifest","no paper or live authority",
                     "test evidence was unavailable to fitting, calibration and model selection"),
        status=TrainingStatus.COMPLETE).with_hash()
    prediction_hash=sha256_lines(p.prediction_hash for p in predictions)
    report=TrainingReportManifest(report_id="sf13_training_report",training_plan_hash=plan.plan_hash,
        dataset_hash=bundle.manifest.dataset_hash,model_artifact_hash=model.artifact_hash,
        calibration_hash=calibration.calibration_hash,prediction_rowset_hash=prediction_hash,
        model_card_hash=card.card_hash,candidate_count=len(evaluations),selected_family=selected.family,
        status=TrainingStatus.COMPLETE,generated_at_utc_msc=generated_at_utc_msc).with_hash()
    return TrainingBundle(transform,model,calibration,tuple(predictions),card,report,tuple(evaluations))
