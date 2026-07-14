from .registry import manifest
from .styles import STYLES
def run():
 m=manifest();return {'phase':m['phase_id']=='FP-I11','version':m['version']=='1.0.0','object_kinds':len(m['object_kinds'])==13,'styles':len(STYLES)>=17,'authority':m['runtime_authority']=='NONE','visual_authority':m['visual_authority']=='CHART_OBJECTS_ONLY'}
