from __future__ import annotations
import argparse,re
from pathlib import Path
TEMPLATE='''#ifndef __{guard}_MQH__\n#define __{guard}_MQH__\n#include <AlphaLab/StrategyFactory/Plugins/SF04_AnatomyPluginBase.mqh>\nclass C{name}Plugin:public CSF04AnatomyPluginBase\n{{\npublic:\n C{name}Plugin(const string symbol):CSF04AnatomyPluginBase({capacity},SF04_QUEUE_REJECT_NEW){{\n  m_descriptor=SF04_DefaultAnatomyDescriptor();\n  m_descriptor.plugin_id="{plugin_id}";\n  m_descriptor.display_name="{display}";\n  m_descriptor.version="0.1.0";\n  m_descriptor.provider_id="alpha_lab";\n  m_descriptor.provider_version="1.0.0";\n  m_descriptor.capability_mask=SF04_CAP_DETERMINISTIC|SF04_CAP_REPLAY_SAFE|SF04_CAP_STATEFUL|SF04_CAP_EMITS_CLUSTER_ID;\n  m_descriptor.update_scope_mask=SF04_UPDATE_NEW_BAR;\n  m_descriptor.event_queue_capacity={capacity};\n  m_descriptor.configuration_schema_hash="cfg_todo";\n  // TODO: declare requirements and bind only shared market services.\n }}\n virtual void ProcessTick(const MqlTick &tick){{}}\n virtual void ProcessTimer(const long now_utc_msc){{}}\n virtual void ProcessClosedBar(const string symbol,const int timeframe_seconds,const SF01_BarRecord &bar){{}}\n}};\n#endif\n'''

def main():
 p=argparse.ArgumentParser();p.add_argument('plugin_id');p.add_argument('--class-name');p.add_argument('--display-name');p.add_argument('--capacity',type=int,default=128);p.add_argument('--output-root',default='mql5/Include/AlphaLab/StrategyFactory/Plugins/Anatomy');a=p.parse_args()
 if not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}',a.plugin_id):raise SystemExit('invalid plugin_id')
 name=a.class_name or ''.join(x.title() for x in re.split(r'[^A-Za-z0-9]+',a.plugin_id) if x)
 display=a.display_name or a.plugin_id
 guard='SF04_'+re.sub(r'[^A-Za-z0-9]','_',a.plugin_id).upper()+'_PLUGIN'
 out=Path(a.output_root)/a.plugin_id.replace('.','_')
 out.mkdir(parents=True,exist_ok=True)
 (out/f'SF04_{name}Plugin.mqh').write_text(TEMPLATE.format(guard=guard,name=name,capacity=a.capacity,plugin_id=a.plugin_id,display=display),encoding='utf-8')
 (out/'ANATOMY_PLUGIN_WORK_PACKET.md').write_text(f'# {display}\n\n- Plugin ID: `{a.plugin_id}`\n- Status: scaffolded\n\n## Required next work\n\n1. Freeze doctrine.\n2. Declare resource requirements.\n3. Implement lifecycle and known-time proof.\n4. Add exact factory registration.\n5. Add golden fixtures and overflow tests.\n',encoding='utf-8')
 print(out)
if __name__=='__main__':main()
