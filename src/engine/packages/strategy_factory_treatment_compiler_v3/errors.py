from __future__ import annotations
class TreatmentCompilerError(ValueError):
    def __init__(self, code:str, message:str, details:dict|None=None):
        super().__init__(f"{code}: {message}")
        self.code=code; self.message=message; self.details=details or {}
class CompatibilityRuleError(TreatmentCompilerError): pass
class CompilationError(TreatmentCompilerError): pass
class PathTransitionError(TreatmentCompilerError): pass
class MatrixBudgetError(TreatmentCompilerError): pass
class ManualBundleError(TreatmentCompilerError): pass
