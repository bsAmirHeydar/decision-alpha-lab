from strategy_factory_validation import *

def _fixture(role=FoldRole.TRAIN,known=1,cluster="c"):
 p=ValidationPlan("p","1",SplitMethod.ANCHORED_WALK_FORWARD,"run","mh","ah","s","space",0,1000,200,100,100,200,10,10,1,1,1).with_hash();f=compile_walk_forward(p)[0]
 r=FoldObservation("o","t","ph",f.fold_id,role,"e",cluster,"out",known,known+1,0.1,0.2,0.1).with_hash();return f,r

def test_known_time_outside_role_is_fatal():
 f,r=_fixture(FoldRole.TRAIN,500);findings=audit_fold_observations((f,),(r,));assert any(x.code=="KNOWN_TIME_OUTSIDE_ROLE" for x in findings)

def test_cluster_cross_role_is_fatal():
 f,r1=_fixture(FoldRole.TRAIN,1,"same");r2=FoldObservation("o2","t","ph",f.fold_id,FoldRole.TEST,"e2","same","out2",f.test.start_utc_msc+1,f.test.start_utc_msc+2,0.1,0.2,0.1).with_hash()
 findings=audit_fold_observations((f,),(r1,r2));assert any(x.code=="CLUSTER_CROSSES_ROLE" for x in findings)
