from strategy_factory_validation import *

def test_report_bundle_is_deterministic(tmp_path):
 e=PromotionEvidence(6,200,0.8,0.02,0.7,0.2,0.99,0.01,0.7,0.03,0.01,0);d=evaluate_promotion("d","p","t",e)
 m=AntiOverfitReportManifest("r","1","p","run","mh","th","sh","spl","str","gate",12,123,"abc")
 a=write_report_bundle(tmp_path/"a",m,d,{"pbo":0.2});b=write_report_bundle(tmp_path/"b",m,d,{"pbo":0.2});assert a==b
