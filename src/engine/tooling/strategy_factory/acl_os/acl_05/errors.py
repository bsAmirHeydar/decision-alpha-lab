class ACL05Error(Exception):
    """Base fail-closed ACL-05 exception carrying a stable reason code."""
    reason_code = "ACL05_ERROR"

    def __init__(self, message: str = "") -> None:
        super().__init__(f"{self.reason_code}: {message}" if message else self.reason_code)

class ContractError(ACL05Error): reason_code = "ACL05_CONTRACT_REJECTED"
class IntegrityError(ACL05Error): reason_code = "ACL05_INTEGRITY_MISMATCH"
class AuthorityError(ACL05Error): reason_code = "ACL05_AUTHORITY_DENIED"
class MutationError(ACL05Error): reason_code = "ACL05_MUTATION_FORBIDDEN"
class KnownTimeError(ACL05Error): reason_code = "ACL05_KNOWN_TIME_VIOLATION"
class StoreError(ACL05Error): reason_code = "ACL05_ARTIFACT_STORE_REJECTED"
class BudgetError(ACL05Error): reason_code = "ACL05_BUDGET_EXCEEDED"
class PublicationError(ACL05Error): reason_code = "ACL05_PUBLICATION_FAILED"
