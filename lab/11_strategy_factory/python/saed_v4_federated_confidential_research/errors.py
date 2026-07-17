class SAEDV433Error(Exception): pass
class ContractError(SAEDV433Error): pass
class UpstreamError(SAEDV433Error): pass
class FederationError(SAEDV433Error): pass
class PrivacyError(SAEDV433Error): pass
class AggregationError(SAEDV433Error): pass
class ProvenanceError(SAEDV433Error): pass
class AuthorityError(SAEDV433Error): pass
