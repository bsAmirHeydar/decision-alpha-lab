class AdvancedTaskError(RuntimeError):
 def __init__(self,code,message,details=None):super().__init__(f'{code}: {message}');self.code=code;self.details=dict(details or {})
class SupportError(AdvancedTaskError):pass
class CensoringError(AdvancedTaskError):pass
class RankingError(AdvancedTaskError):pass
class PolicyError(AdvancedTaskError):pass
