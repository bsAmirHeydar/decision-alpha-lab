class SequenceStateSpaceError(ValueError): """Fail-closed base error for SAED V4-12."""
class ContractError(SequenceStateSpaceError): pass
class AuthorityError(SequenceStateSpaceError): pass
class IntegrityError(SequenceStateSpaceError): pass
class CausalityError(SequenceStateSpaceError): pass
class ResetError(SequenceStateSpaceError): pass
class NumericalError(SequenceStateSpaceError): pass
class BudgetError(SequenceStateSpaceError): pass
class ParityError(SequenceStateSpaceError): pass
class TrainingError(SequenceStateSpaceError): pass
class RegistryError(SequenceStateSpaceError): pass
class DistillationError(SequenceStateSpaceError): pass
