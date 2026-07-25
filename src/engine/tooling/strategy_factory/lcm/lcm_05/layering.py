from .registries import ALLOWED_EDGES
ROLE_TO_LAYER={"CONTEXT":"CONTEXT","SETUP":"SETUP","TREATMENT":"TREATMENT","VISUALIZER":"VISUALIZER","SHARED_PRIMITIVE":"SHARED_ENGINE","PLATFORM_ADAPTER":"PLATFORM_ADAPTER","EXECUTION_ADAPTER":"EXECUTION_ADAPTER","PLATFORM_KERNEL":"APPLICATION","GENERATED_PROJECTION":"GENERATED","RELEASE_METADATA":"RELEASE","SOURCE_EVIDENCE":"EVIDENCE","DOCUMENTATION":"EVIDENCE","TEST_CODE":"MIGRATION_CONTROL","TEST_FIXTURE":"EVIDENCE","CONFIGURATION_CONTRACT":"EVIDENCE","GOVERNANCE_CONTROL":"MIGRATION_CONTROL","RESEARCH":"APPLICATION","DIAGNOSTIC":"APPLICATION","ARCHIVE":"EVIDENCE","UNKNOWN_ROLE":"EVIDENCE"}
def layer_for(role,path=''):
    if str(path).startswith('src/engine/tooling/strategy_factory/lcm/') or '/migration/' in str(path):return 'MIGRATION_CONTROL'
    return ROLE_TO_LAYER.get(role,'EVIDENCE')
def allowed(source_layer,target_layer):return target_layer in ALLOWED_EDGES[source_layer]
def layer_graph():
    nodes=sorted(ALLOWED_EDGES);edges=[]
    for s,targets in ALLOWED_EDGES.items():
        for t in sorted(targets):
            if s!=t:edges.append({"source_layer":s,"target_layer":t})
    return nodes,edges
def is_acyclic(nodes,edges):
    graph={n:set() for n in nodes}
    for e in edges:graph[e['source_layer']].add(e['target_layer'])
    visiting=set();done=set()
    def dfs(n):
        if n in visiting:return False
        if n in done:return True
        visiting.add(n)
        for m in graph[n]:
            if not dfs(m):return False
        visiting.remove(n);done.add(n);return True
    return all(dfs(n) for n in nodes)
