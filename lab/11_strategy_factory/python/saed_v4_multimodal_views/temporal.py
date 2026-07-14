from .canonical import parse_time
def validate_boundary(event_time:str,known_time:str,known_as_of:str,event_as_of:str)->None:
    et=parse_time(event_time);kt=parse_time(known_time);ka=parse_time(known_as_of);ea=parse_time(event_as_of)
    if kt<et:raise ValueError('known_time before event_time')
    if kt>ka:raise ValueError('source not known at boundary')
    if et>ea:raise ValueError('source event after event_as_of')
def age_ms(event_time:str,event_as_of:str)->int:return max(0,int((parse_time(event_as_of)-parse_time(event_time)).total_seconds()*1000))
