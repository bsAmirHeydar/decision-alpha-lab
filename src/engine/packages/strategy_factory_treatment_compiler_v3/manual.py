from __future__ import annotations
from dataclasses import replace
from .contracts import ManualTreatmentBundle
from .errors import ManualBundleError
class ManualTreatmentCompiler:
    def __init__(self,compiler): self.compiler=compiler
    def compile(self,bundle:ManualTreatmentBundle,context):
        if not bundle.frozen: raise ManualBundleError('bundle_not_frozen','manual bundle must be frozen before compilation')
        if not bundle.draft.pinned: raise ManualBundleError('draft_not_pinned','manual draft must be pinned')
        treatment,report=self.compiler.compile(bundle.draft,context)
        if bundle.expected_treatment_id and treatment.treatment_id!=bundle.expected_treatment_id:
            raise ManualBundleError('manual_parity_mismatch','compiled treatment differs from pinned baseline',{'expected':bundle.expected_treatment_id,'actual':treatment.treatment_id})
        return treatment,report
