from strategy_factory_validation import build_knn_edges,evaluate_surface_stability

def test_plateau_has_support():
 vectors={"a":(0.,0.),"b":(1.,0.),"c":(0.,1.),"d":(1.,1.)};metrics={"a":1.0,"b":0.9,"c":0.85,"d":0.8}
 edges=build_knn_edges(vectors,2);r=evaluate_surface_stability(metrics,edges,"a");assert r.neighbor_count>=2;assert r.support_score>0
