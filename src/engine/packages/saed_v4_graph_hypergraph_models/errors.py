class GraphHypergraphError(ValueError): """Fail-closed base error for SAED V4-13."""
class ContractError(GraphHypergraphError): pass
class AuthorityError(GraphHypergraphError): pass
class IntegrityError(GraphHypergraphError): pass
class CausalityError(GraphHypergraphError): pass
class TopologyError(GraphHypergraphError): pass
class NumericalError(GraphHypergraphError): pass
class BudgetError(GraphHypergraphError): pass
class ContaminationError(GraphHypergraphError): pass
class TrainingError(GraphHypergraphError): pass
class RegistryError(GraphHypergraphError): pass
class ReplayError(GraphHypergraphError): pass
