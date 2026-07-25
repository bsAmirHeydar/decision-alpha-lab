from __future__ import annotations
from dataclasses import replace
from typing import Iterable,Mapping
from .contracts import RuntimeBundleManifest,ArtifactRef,PreprocessingContract,NativeModelArtifact,ExportRecord
from .enums import RuntimeMode
from .errors import BundleValidationError
REQUIRED_ROLES=('context_package','feature_schema','preprocessing','model','calibration','policy_graph','manual_policy','fallback_policy','authority_matrix','treatment_registry','risk_policy','monitoring_policy','rollback_target')
def validate_bundle(manifest:RuntimeBundleManifest,preprocessing:PreprocessingContract,model:NativeModelArtifact,export:ExportRecord,available_artifacts:Mapping[str,str]|None=None)->None:
    roles={c.role:c for c in manifest.components}
    missing=[r for r in REQUIRED_ROLES if r not in roles]
    if missing:raise BundleValidationError('partial_bundle','required bundle roles missing',{'missing':missing})
    if manifest.preprocessing_hash!=preprocessing.preprocessing_hash:raise BundleValidationError('preprocessing_hash_mismatch','manifest preprocessing hash mismatch')
    if manifest.model_hash!=model.model_hash or export.model_hash!=model.model_hash:raise BundleValidationError('model_hash_mismatch','model identity mismatch')
    if manifest.export_hash!=export.export_hash:raise BundleValidationError('export_hash_mismatch','export identity mismatch')
    if manifest.feature_order!=preprocessing.feature_order:raise BundleValidationError('feature_order_mismatch','manifest and preprocessing feature order differ')
    if model.input_names!=preprocessing.output_names:raise BundleValidationError('model_input_order_mismatch','model input names differ from preprocessing output order')
    if manifest.output_names!=model.output_names:raise BundleValidationError('model_output_order_mismatch','manifest output names differ from model')
    if available_artifacts is not None:
        for role,ref in roles.items():
            actual=available_artifacts.get(role)
            if ref.required and actual is None:raise BundleValidationError('missing_artifact',f'missing artifact for {role}')
            if actual is not None and actual!=ref.sha256:raise BundleValidationError('artifact_hash_mismatch',f'artifact mismatch for {role}',{'expected':ref.sha256,'actual':actual})

def compile_bundle(*,bundle_id:str,version:str,generation:int,created_at_ms:int,components:Iterable[ArtifactRef],preprocessing:PreprocessingContract,model:NativeModelArtifact,export:ExportRecord,policy_graph_hash:str,manual_policy_hash:str,fallback_policy_hash:str,authority_matrix_hash:str,monitoring_policy_hash:str,rollback_bundle_hash:str,allowed_modes:tuple[RuntimeMode,...],signature_key_id:str,limitations:tuple[str,...]=())->RuntimeBundleManifest:
    manifest=RuntimeBundleManifest(bundle_id,version,generation,created_at_ms,tuple(sorted(components,key=lambda c:c.role)),preprocessing.preprocessing_hash,model.model_hash,export.export_hash,policy_graph_hash,manual_policy_hash,fallback_policy_hash,authority_matrix_hash,monitoring_policy_hash,rollback_bundle_hash,allowed_modes,preprocessing.feature_order,model.output_names,signature_key_id,'',limitations)
    validate_bundle(manifest,preprocessing,model,export)
    return manifest
