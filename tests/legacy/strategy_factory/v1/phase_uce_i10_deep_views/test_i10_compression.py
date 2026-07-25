from strategy_factory_deep_views_v3.compression import distill_linear,quantize_symmetric_int8
def test_distillation_and_quantization_report_parity():
    x=[(float(i),float(i%2)) for i in range(30)];teacher=[.5*a+.2*b for a,b in x];coef,report=distill_linear('teacher','student',x,teacher,.8,10,max_fidelity_mae=.001);assert report.accepted
    q,scale,qr=quantize_symmetric_int8(coef,max_error=.05);assert qr.accepted;assert len(q)==len(coef);assert scale>0
