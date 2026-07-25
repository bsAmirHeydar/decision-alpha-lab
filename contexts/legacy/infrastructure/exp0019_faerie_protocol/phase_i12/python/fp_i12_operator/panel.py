from math import ceil
from .contracts import *
from .canonical import stable_id,sha256

def _metric(k,l,v,s='INFO'):return PanelMetric(k,l,str(v),s)
def build_panel(snapshot,filtered,cfg,page=0):
    total=len(filtered.included); pages=max(1,ceil(total/cfg.page_size));page=max(0,min(page,pages-1));start=page*cfg.page_size;visible=filtered.included[start:start+cfg.page_size]
    counts={}
    for item in snapshot.items:
        counts[item.disposition]=counts.get(item.disposition,0)+1
    sections=[
      PanelSection('overview','Context',(
       _metric('health','Health',snapshot.health.value,'CRITICAL' if snapshot.health is OperatorHealth.BLOCKED else 'WARNING' if snapshot.health is OperatorHealth.DEGRADED else 'INFO'),
       _metric('data','Data',snapshot.data_readiness),_metric('revision','Revision',snapshot.source_revision_sequence),_metric('ledger','Ledger events',snapshot.ledger_event_count))),
      PanelSection('ww','Weekly WW',(_metric('ww_direction','Active direction',snapshot.active_ww_direction),)),
      PanelSection('quota','Pair-Session Quota',(_metric('winner','Winner',snapshot.quota_winner_signal_id or 'NONE'),_metric('quota_suppressed','Suppressed',counts.get('SUPPRESSED_BY_QUOTA',0)))),
      PanelSection('signals','Signals',(_metric('total','Total',len(snapshot.items)),_metric('visible','Visible',total),_metric('ww_suppressed','WW suppressed',counts.get('SUPPRESSED_BY_WW',0)),_metric('blocked','Blocked',counts.get('BLOCKED',0)))),
    ]
    if cfg.show_open_decisions:
      sections.append(PanelSection('decisions','Open Decisions',(_metric('fp_dec_012',OPEN_DECISION_ID,snapshot.open_decision_state,'WARNING' if snapshot.open_decision_state=='UNSET' else 'INFO'),)))
    payload={'instance_id':'','mode':cfg.mode.value,'state':cfg.state.value,'dock':cfg.dock.value,'page':page,'pages':pages,'sections':sections,'visible':[x.semantic_id for x in visible]}
    ph=sha256(payload);return PanelModel(stable_id('FPPANEL',payload),'',cfg.mode,cfg.state,cfg.dock,page,pages,total,tuple(sections),tuple(x.semantic_id for x in visible),ph)

def bind_panel_instance(panel,instance_id):
    payload={'panel_hash':panel.panel_hash,'instance_id':instance_id};return PanelModel(stable_id('FPPANEL',payload),instance_id,panel.mode,panel.state,panel.dock,panel.page,panel.page_count,panel.total_items,panel.sections,panel.visible_item_ids,sha256(payload))
