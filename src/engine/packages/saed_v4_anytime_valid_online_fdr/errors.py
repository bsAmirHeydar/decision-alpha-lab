class SAEDV428Error(Exception):
    """Base error for the V4-28 closed online-FDR research reference."""
class ContractError(SAEDV428Error): pass
class IntegrityError(SAEDV428Error): pass
class EvidenceError(SAEDV428Error): pass
class WealthError(SAEDV428Error): pass
class ProcedureError(SAEDV428Error): pass
class AuthorityBoundaryError(SAEDV428Error): pass
