FORBIDDEN=('OrderSend','CTrade','PositionOpen','PositionClose','WebRequest','FileOpen','Socket','PERIOD_CURRENT')
def scan_text(text): return tuple(x for x in FORBIDDEN if x in text)
def runtime_authority(): return 'NONE'
def visual_authority(): return 'CHART_OBJECTS_ONLY'
