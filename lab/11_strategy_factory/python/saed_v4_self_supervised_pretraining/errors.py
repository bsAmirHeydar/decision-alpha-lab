class SelfSupervisedPretrainingError(ValueError):
    """Base fail-closed error for SAED V4-11."""
class ContractError(SelfSupervisedPretrainingError): pass
class AuthorityError(SelfSupervisedPretrainingError): pass
class IntegrityError(SelfSupervisedPretrainingError): pass
class LeakageError(SelfSupervisedPretrainingError): pass
class ContaminationError(SelfSupervisedPretrainingError): pass
class SplitError(SelfSupervisedPretrainingError): pass
class BudgetError(SelfSupervisedPretrainingError): pass
class TrainingError(SelfSupervisedPretrainingError): pass
class CheckpointError(SelfSupervisedPretrainingError): pass
class EvaluationError(SelfSupervisedPretrainingError): pass
class RegistryError(SelfSupervisedPretrainingError): pass
