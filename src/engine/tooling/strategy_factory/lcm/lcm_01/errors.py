class LCM01Error(RuntimeError):
    """Base error for LCM-01."""

class ContractViolation(LCM01Error):
    """A closed contract was violated."""

class IntegrityError(LCM01Error):
    """Input or output integrity failed."""

class SurveyError(LCM01Error):
    """Survey execution could not complete deterministically."""
