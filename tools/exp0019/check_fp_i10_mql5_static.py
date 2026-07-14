from pathlib import Path
import json,sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
inc=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I10'; ind=root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5'
files=list(inc.glob('*.mqh'))
text=ind.read_text(encoding='utf-8')
checks={'include_count':len(files)>=10,'all_guards':all('#ifndef' in p.read_text(encoding='utf-8') for p in files),'indicator_buffers_12':'#property indicator_buffers 12' in text,'draw_none':text.count('DRAW_NONE')>=12,'lifecycle_handlers':all(x in text for x in ['OnInit(','OnCalculate(','OnTimer(','OnChartEvent(','OnDeinit(']),'no_dynamic_current':'PERIOD_CURRENT' not in text,'instance_shortname':'IndicatorSetString' in text}
print(json.dumps(checks,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
