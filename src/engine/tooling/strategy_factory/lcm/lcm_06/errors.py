class LCM06Error(RuntimeError): pass
class IntegrityError(LCM06Error): pass
class PolicyError(LCM06Error): pass
class PathSafetyError(LCM06Error): pass
class PacketValidationError(LCM06Error): pass
class TraceComparisonError(LCM06Error): pass
