from __future__ import annotations
class TreatmentError(ValueError):
    def __init__(self, code: str, message: str, details: dict | None=None):
        super().__init__(f"{code}: {message}")
        self.code=code; self.message=message; self.details=details or {}
class RegistryError(TreatmentError): pass
class ParameterError(TreatmentError): pass
class GeometryError(TreatmentError): pass
class CompatibilityError(TreatmentError): pass
