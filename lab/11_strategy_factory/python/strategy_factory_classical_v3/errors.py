class ClassicalPackError(RuntimeError):
 def __init__(self,code,message,details=None):super().__init__(message);self.code=code;self.details=details or {}
class DependencyUnavailableError(ClassicalPackError):pass
class AlgorithmConfigurationError(ClassicalPackError):pass
class ExplanationLeakageError(ClassicalPackError):pass
class ComparisonGateError(ClassicalPackError):pass
