class LCM09BError(RuntimeError): pass
class ContractError(LCM09BError): pass
class IntegrityError(LCM09BError): pass
class AuthorityError(LCM09BError): pass
class ReplayError(LCM09BError): pass
