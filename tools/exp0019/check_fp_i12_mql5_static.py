from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
base=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12'
required=['FP_I12_All.mqh','FP_IndicatorPanel.mqh','FP_AlertRouter.mqh','FP_AuditExporter.mqh','FP_I12_OperatorUX.mqh']
checks=[(base/x).exists() for x in required]
prod=(root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5').read_text(encoding='utf-8')
checks += ['I12/FP_I12_All.mqh' in prod,'g_operator.OnSnapshot' in prod,'g_operator.OnChartEvent' in prod]
print({'checks':checks});raise SystemExit(0 if all(checks) else 1)
