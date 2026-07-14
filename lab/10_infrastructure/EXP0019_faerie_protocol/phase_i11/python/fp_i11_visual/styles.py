from .contracts import Style
from .enums import ObjectKind,SignalDisposition,SemanticState
STYLES={
 'SESSION_A':Style('SESSION_A','#8A5CF6','#8A5CF6',1,'SOLID',28,8,20),
 'SESSION_L':Style('SESSION_L','#00A8E8','#00A8E8',1,'SOLID',24,8,20),
 'SESSION_N':Style('SESSION_N','#F59E0B','#F59E0B',1,'SOLID',22,8,20),
 'WEEK':Style('WEEK','#6B7280','#6B7280',1,'DASH',12,8,10),
 'REF_HIGH':Style('REF_HIGH','#EF4444','#000000',1,'DASH',220,8,30),
 'REF_LOW':Style('REF_LOW','#22C55E','#000000',1,'DASH',220,8,30),
 'HUNT':Style('HUNT','#F97316','#000000',2,'SOLID',255,9,40),
 'CANDIDATE':Style('CANDIDATE','#FBBF24','#000000',1,'DOT',210,9,50),
 'CONFIRMED_BULL':Style('CONFIRMED_BULL','#22C55E','#000000',2,'SOLID',255,10,50),
 'CONFIRMED_BEAR':Style('CONFIRMED_BEAR','#EF4444','#000000',2,'SOLID',255,10,50),
 'INVALID':Style('INVALID','#9CA3AF','#000000',1,'DOT',190,8,50),
 'WW_BULL':Style('WW_BULL','#16A34A','#16A34A',2,'SOLID',25,10,15),
 'WW_BEAR':Style('WW_BEAR','#DC2626','#DC2626',2,'SOLID',25,10,15),
 'SUPPRESSED_WW':Style('SUPPRESSED_WW','#A855F7','#000000',1,'DOT',180,9,60),
 'SUPPRESSED_QUOTA':Style('SUPPRESSED_QUOTA','#64748B','#000000',1,'DOT',160,9,60),
 'WINNER':Style('WINNER','#FACC15','#000000',3,'SOLID',255,11,70),
 'HEALTH_READY':Style('HEALTH_READY','#16A34A','#0F172A',1,'SOLID',230,9,80),
 'HEALTH_DEGRADED':Style('HEALTH_DEGRADED','#F59E0B','#0F172A',1,'SOLID',230,9,80),
 'HEALTH_BLOCKED':Style('HEALTH_BLOCKED','#DC2626','#0F172A',1,'SOLID',230,9,80),
}
def style_for_window(kind): return STYLES.get(f'SESSION_{kind}',STYLES['WEEK'])
def style_for_reference(side): return STYLES['REF_HIGH' if side=='HIGH' else 'REF_LOW']
def style_for_signal(direction,state,disposition):
 if disposition is SignalDisposition.QUOTA_WINNER:return STYLES['WINNER']
 if disposition is SignalDisposition.SUPPRESSED_BY_WW:return STYLES['SUPPRESSED_WW']
 if disposition is SignalDisposition.SUPPRESSED_BY_QUOTA:return STYLES['SUPPRESSED_QUOTA']
 if state is SemanticState.CONFIRMED:return STYLES['CONFIRMED_BULL' if direction=='BULLISH' else 'CONFIRMED_BEAR']
 if state is SemanticState.INVALIDATED:return STYLES['INVALID']
 return STYLES['CANDIDATE']
