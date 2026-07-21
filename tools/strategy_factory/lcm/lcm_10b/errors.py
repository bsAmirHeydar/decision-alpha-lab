class LCM10BError(RuntimeError): pass
class IntegrityError(LCM10BError): pass
class ContractError(LCM10BError): pass
class IntentValidationError(LCM10BError): pass
class CapabilityDeniedError(LCM10BError): pass
class TranslationBlockedError(LCM10BError): pass
class VerificationError(LCM10BError): pass
