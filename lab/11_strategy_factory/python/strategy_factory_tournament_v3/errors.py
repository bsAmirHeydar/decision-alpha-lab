class TournamentError(ValueError):
 def __init__(self,code:str,message:str,evidence:dict|None=None):super().__init__(message);self.code=code;self.evidence=evidence or {}
