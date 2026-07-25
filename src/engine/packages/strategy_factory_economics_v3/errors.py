class EconomicsError(ValueError):
    def __init__(self,code,message,evidence=None):
        super().__init__(message); self.code=code; self.message=message; self.evidence=evidence or {}
    def to_dict(self): return {'code':self.code,'message':self.message,'evidence':self.evidence}
class StaleEconomicInput(EconomicsError): pass
class BrokerConstraintError(EconomicsError): pass
class InsufficientRiskBudget(EconomicsError): pass
class ReservationError(EconomicsError): pass
