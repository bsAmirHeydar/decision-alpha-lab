#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Qualification'
EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'
errors=[]
required=['QualificationCatalog.mqh','QualificationGate.mqh','QualificationCompileEvidence.mqh','QualificationDifferentialEvidence.mqh','QualificationSoakEvidence.mqh','QualificationChaosEvidence.mqh','QualificationRecoveryEvidence.mqh','QualificationSecurityEvidence.mqh','QualificationProspectiveStage.mqh','QualificationReleaseManifest.mqh','QualificationReconciliationGuard.mqh','QualificationKillSwitch.mqh','QualificationArtifactVerifier.mqh']
for name in required:
 if not (INC/name).exists(): errors.append('missing:'+name)
cat=(INC/'QualificationCatalog.mqh').read_text() if (INC/'QualificationCatalog.mqh').exists() else ''
for token in ('AL_QUALIFICATION_ORDER_AUTHORITY false','AL_QUALIFICATION_BROKER_AUTHORITY false','AL_QUALIFICATION_NETWORK_AUTHORITY false'):
 if token not in cat: errors.append('authority_boundary:'+token)
for path in EXP.glob('EXP_UCE_I18_*.mq5'):
 text=path.read_text()
 for token in ('OrderSend(','CTrade','trade.Buy','trade.Sell'):
  if token in text: errors.append(f'forbidden_order_api:{path.name}:{token}')
print(json.dumps({'phase':'UCE-I18','status':'pass' if not errors else 'fail','include_count':len(list(INC.glob('*.mqh'))),'diagnostic_count':len(list(EXP.glob('EXP_UCE_I18_*.mq5'))),'errors':errors},indent=2))
raise SystemExit(1 if errors else 0)
