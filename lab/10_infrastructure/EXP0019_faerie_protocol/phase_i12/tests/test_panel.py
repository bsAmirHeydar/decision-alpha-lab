from fp_i12_operator import *
def test_panel_sections(snapshot,config):
 f=apply_filters(snapshot.items,config.filters,snapshot.computed_hash);p=build_panel(snapshot,f,config.panel);assert {x.section_id for x in p.sections}>={'overview','ww','quota','signals','decisions'}
def test_open_decision_visible(snapshot,config):
 p=build_panel(snapshot,apply_filters(snapshot.items,config.filters,snapshot.computed_hash),config.panel);assert any(m.value=='UNSET' for s in p.sections for m in s.metrics)
def test_paging(snapshot):
 c=PanelConfig(page_size=1);f=apply_filters(snapshot.items,FilterConfig(),snapshot.computed_hash);p=build_panel(snapshot,f,c,2);assert p.page==2 and len(p.visible_item_ids)==1
def test_bind_instance(snapshot,config):
 p=bind_panel_instance(build_panel(snapshot,apply_filters(snapshot.items,config.filters,snapshot.computed_hash),config.panel),config.instance_id);assert p.instance_id==config.instance_id
