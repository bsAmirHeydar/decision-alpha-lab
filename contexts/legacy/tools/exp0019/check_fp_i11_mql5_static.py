from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
inc=root/'mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I11'
prod=root/'mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5'
selft=root/'mql5/Tests/Indicators/EXP0019/FaerieProtocol/EXP0019_FP_I11_VisualSelfTest.mq5'
files=list(inc.glob('*.mqh'));pt=prod.read_text(encoding='utf-8');st=selft.read_text(encoding='utf-8')
all_text='\n'.join(p.read_text(encoding='utf-8') for p in files+[prod,selft])
checks={
 'include_count':len(files)>=10,
 'include_guards':all('#ifndef' in p.read_text(encoding='utf-8') and '#endif' in p.read_text(encoding='utf-8') for p in files),
 'object_kind_count':'ObjectKindCount(){return 13;}' in (inc/'FP_I11_Registry.mqh').read_text(encoding='utf-8'),
 'dirty_set_manager':'FP_I11_ObjectManager' in (inc/'FP_I11_ObjectManager.mqh').read_text(encoding='utf-8'),
 'unchanged_no_recreate':'m_stats.unchanged++' in (inc/'FP_I11_ObjectManager.mqh').read_text(encoding='utf-8'),
 'immutable_guard':'m_immutable[idx]' in (inc/'FP_I11_ObjectManager.mqh').read_text(encoding='utf-8'),
 'production_integration':'FP_I11_VisualEngine' in pt and 'BeginFrame' in pt and 'EndFrame' in pt,
 'self_test_all_families':all(x in st for x in ['ProjectWindow','ProjectReference','ProjectHunt','ProjectSignal','ProjectWW']),
 'i10_buffers_preserved':'#property indicator_buffers 12' in pt and pt.count('DRAW_NONE')>=12,
 'no_period_current':'PERIOD_CURRENT' not in all_text,
}
print(json.dumps(checks,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
