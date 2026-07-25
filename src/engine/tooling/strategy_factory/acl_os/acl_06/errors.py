class ACL06Error(Exception):
    reason_code="ACL06_ERROR"
    def __init__(self,message: str="") -> None:
        super().__init__(f"{self.reason_code}: {message}" if message else self.reason_code)
class ContractError(ACL06Error): reason_code="ACL06_CONTRACT_REJECTED"
class IntegrityError(ACL06Error): reason_code="ACL06_INTEGRITY_MISMATCH"
class AuthorityError(ACL06Error): reason_code="ACL06_AUTHORITY_DENIED"
class DAGError(ACL06Error): reason_code="ACL06_DAG_REJECTED"
class TaskError(ACL06Error): reason_code="ACL06_TASK_FAILED"
class BudgetError(ACL06Error): reason_code="ACL06_BUDGET_EXCEEDED"
class KnownTimeError(ACL06Error): reason_code="ACL06_KNOWN_TIME_VIOLATION"
class CacheError(ACL06Error): reason_code="ACL06_CACHE_REJECTED"
class PublicationError(ACL06Error): reason_code="ACL06_PUBLICATION_FAILED"
