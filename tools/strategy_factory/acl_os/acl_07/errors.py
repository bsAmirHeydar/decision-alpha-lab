class ACL07Error(Exception):
    reason_code="ACL07_ERROR"
    def __init__(self,message: str="") -> None:
        super().__init__(f"{self.reason_code}: {message}" if message else self.reason_code)
class ContractError(ACL07Error): reason_code="ACL07_CONTRACT_REJECTED"
class IntegrityError(ACL07Error): reason_code="ACL07_INTEGRITY_MISMATCH"
class AuthorityError(ACL07Error): reason_code="ACL07_AUTHORITY_DENIED"
class EvidenceError(ACL07Error): reason_code="ACL07_EVIDENCE_REJECTED"
class GateError(ACL07Error): reason_code="ACL07_GATE_FAILED"
class PolicyError(ACL07Error): reason_code="ACL07_POLICY_REJECTED"
class PublicationError(ACL07Error): reason_code="ACL07_PUBLICATION_FAILED"
