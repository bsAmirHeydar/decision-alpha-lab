from fp_i10_indicator import *

def test_two_instances_isolated(config,modules):
 e1=IndicatorEngine(); e2=IndicatorEngine(); now=1783900800000; e1.initialize(config=config,chart_id=10,terminal_instance_id='T',modules=modules,now_m1=now); e2.initialize(config=config,chart_id=11,terminal_instance_id='T',modules=modules,now_m1=now); assert e1.instance.instance_id!=e2.instance.instance_id and e1.instance.object_namespace!=e2.instance.object_namespace
def test_events_do_not_cross(config,modules):
 e1=IndicatorEngine(); e2=IndicatorEngine(); now=1783900800000; e1.initialize(config=config,chart_id=10,terminal_instance_id='T',modules=modules,now_m1=now); e2.initialize(config=config,chart_id=11,terminal_instance_id='T',modules=modules,now_m1=now); e1.chart_event(now_m1=now,event_id=1); assert len(e1.event_chain.events)==len(e2.event_chain.events)+1
