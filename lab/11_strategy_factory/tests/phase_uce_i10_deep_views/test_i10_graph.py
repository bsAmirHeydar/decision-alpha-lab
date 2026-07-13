import pytest
from strategy_factory_deep_views_v3.golden import graph_spec,graph_case
from strategy_factory_deep_views_v3.graph import build_graph_artifact,GraphMessagePassingModel
from strategy_factory_deep_views_v3.errors import DeepViewError
def test_graph_topology_and_model_are_deterministic():
    values,targets,n,p,edges=graph_case();spec=graph_spec();nodes=tuple(f'n{i}' for i in range(n));features=tuple(tuple(values[0][i*p:(i+1)*p]) for i in range(n));a=build_graph_artifact(spec,'ctx',100,nodes,tuple(range(n)),features,edges);b=build_graph_artifact(spec,'ctx',100,nodes,tuple(range(n)),features,tuple(reversed(edges)))
    assert a.topology_hash==b.topology_hash
    m1=GraphMessagePassingModel.fit(values,targets,n,p,edges);m2=GraphMessagePassingModel.fit(values,targets,n,p,edges);assert m1.state_hash==m2.state_hash
def test_graph_rejects_future_node():
    spec=graph_spec()
    with pytest.raises(DeepViewError,match='future'):
        build_graph_artifact(spec,'ctx',10,('a',),(11,),((1,2,3),),())
