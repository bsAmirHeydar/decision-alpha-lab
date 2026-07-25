from .errors import TournamentError
SUPPORTED={'1.0.0'}
def migrate(payload:dict,target='1.0.0')->dict:
 version=payload.get('version')
 if version not in SUPPORTED:raise TournamentError('unsupported_version','explicit migration required',{'version':version})
 if target!='1.0.0':raise TournamentError('unsupported_target_version','unsupported target',{'target':target})
 return dict(payload)
