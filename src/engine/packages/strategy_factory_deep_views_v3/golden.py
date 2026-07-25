from .canonical import canonical_sha256,stable_id
from .contracts import RasterSpec,GraphSpec,SeedRunObservation,ViewAblationObservation,ExportAssessment
from .enums import ExportPath

def sequence_case(n=48,steps=8,channels=2):
    values=[];targets=[]
    for i in range(n):
        seq=[]
        for t in range(steps):
            a=.05*i+.2*t+(.1 if i%2 else -.1);b=.03*i-.1*t+(.2 if i%3==0 else 0);seq.extend((a,b))
        values.append(tuple(seq));targets.append((seq[-2]-.5*seq[-1],))
    return tuple(values),tuple(targets),(steps,channels)

def candles(n=30,start_time=1000):
    out=[];p=100.0
    for i in range(n):
        o=p;cl=o+(.6 if i%3 else -.25)+.02*i;h=max(o,cl)+.2;l=min(o,cl)-.15;out.append({'time_ms':start_time+i*60000,'open':o,'high':h,'low':l,'close':cl,'volume':100+i});p=cl
    return tuple(out)

def raster_spec():return RasterSpec('golden_chart','1.0.0',24,20,('wick','body','direction'),'window_min_max','none',canonical_sha256({'augmentation':'none'}))
def graph_spec():return GraphSpec('golden_graph','1.0.0',('price_delta','age','relation'),False,2,'topology_v1')
def graph_case(n=36,node_count=5,feature_count=3):
    edges=((0,1),(1,2),(2,3),(3,4),(0,4));values=[];targets=[]
    for i in range(n):
        v=[]
        for j in range(node_count):v.extend((.1*i+.2*j,float(j),1.0 if (i+j)%2 else -1.0))
        values.append(tuple(v));targets.append((.3*v[0]+.1*v[-3],))
    return tuple(values),tuple(targets),node_count,feature_count,edges

def qualification_evidence():
    seeds=tuple(SeedRunObservation(s,'succeeded',.64+.005*s,.35+.01*s,.04,120+s,2,'artifact_'+str(s)) for s in (11,17,23))
    ab=(ViewAblationObservation('sequence',.65,.60,.05,.04,True,canonical_sha256({'view':'sequence'})),)
    mat={'path':'onnx','available':True,'parity':0.0,'latency':2.1,'artifact':'export_hash'}
    export=ExportAssessment(ExportPath.ONNX,True,0.0,2.1,'export_hash','verified_reference',canonical_sha256(mat))
    return seeds,ab,export
