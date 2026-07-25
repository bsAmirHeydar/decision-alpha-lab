#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json

ROOT=find_repository_root(__file__)
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Operations'
EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'
errors=[]
required=[
'OperationsCatalog.mqh','OperationsEnums.mqh','OperationsHashGuard.mqh','OperationsReleaseBinding.mqh',
'OperationsTargetBinding.mqh','OperationsRiskEnvelope.mqh','OperationsRuntimeLease.mqh','OperationsTelemetry.mqh',
'OperationsHealthGate.mqh','OperationsReconciliationGuard.mqh','OperationsIncidentGate.mqh',
'OperationsCycleAuthorization.mqh','OperationsRampGate.mqh','OperationsKillSwitch.mqh',
'OperationsRollbackGuard.mqh','OperationsEodGuard.mqh','OperationsChangeGuard.mqh','OperationsRetirementGuard.mqh']
for name in required:
    if not (INC/name).exists(): errors.append('missing:'+name)
catalog=(INC/'OperationsCatalog.mqh').read_text(encoding='utf-8') if (INC/'OperationsCatalog.mqh').exists() else ''
for token in ('AL_OPERATIONS_ORDER_AUTHORITY false','AL_OPERATIONS_BROKER_AUTHORITY false','AL_OPERATIONS_NETWORK_AUTHORITY false','AL_OPERATIONS_REFERENCE_ACTIVATION false'):
    if token not in catalog: errors.append('authority_boundary:'+token)
for path in list(INC.glob('*.mqh'))+list(EXP.glob('EXP_UCE_I19_*.mq5')):
    text=path.read_text(encoding='utf-8')
    for token in ('OrderSend(','CTrade','trade.Buy','trade.Sell','WebRequest(','WinExec','ShellExecute'):
        if token in text: errors.append(f'forbidden_api:{path.name}:{token}')
print(json.dumps({'phase':'UCE-I19','status':'pass' if not errors else 'fail','include_count':len(list(INC.glob('*.mqh'))),'diagnostic_count':len(list(EXP.glob('EXP_UCE_I19_*.mq5'))),'errors':errors},indent=2))
raise SystemExit(1 if errors else 0)
