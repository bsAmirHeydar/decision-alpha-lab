class LCM10CError(RuntimeError): pass
class IntegrityError(LCM10CError): pass
class SafetyControlRejection(LCM10CError): pass
class AuthorityDenied(LCM10CError): pass
class VerificationError(LCM10CError): pass
