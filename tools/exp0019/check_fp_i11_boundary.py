from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
paths=[root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I11',root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5',root/'mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I11_VisualSelfTest.mq5']
files=[]
for p in paths:
    files.extend(p.glob('*.mqh') if p.is_dir() else [p])
text='\n'.join(p.read_text(encoding='utf-8') for p in files if p.exists())
forbidden=['OrderSend','CTrade','PositionOpen','PositionClose','WebRequest','SocketCreate','TRADE_ACTION_','FP_I09_CONSUMED','FP_I09_RELEASED']
found=[x for x in forbidden if x in text]
checks={'no_trade_or_network_authority':not found,'visual_object_authority':'ObjectCreate' in text,'instance_namespace':'FP19::' in text,'no_period_current':'PERIOD_CURRENT' not in text}
print(json.dumps({'checks':checks,'forbidden_found':found},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
