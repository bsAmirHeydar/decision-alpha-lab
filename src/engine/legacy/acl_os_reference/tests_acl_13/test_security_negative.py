import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_13.io import safe_relative
from src.engine.tooling.strategy_factory.acl_os.acl_13.errors import ContractError,PublicationError
from src.engine.tooling.strategy_factory.acl_os.acl_13.service import ACL13OneHourAssessmentService
def test_path_escape_denied(tmp_path):
    with pytest.raises(ContractError): safe_relative(tmp_path,'../escape')
def test_absolute_path_denied(tmp_path):
    with pytest.raises(ContractError): safe_relative(tmp_path,'/etc/passwd')
def test_non_empty_destination_denied(tmp_path,acl12,permit,assessment_request,budget):
    out=tmp_path/'out'; out.mkdir(); (out/'x').write_text('x')
    with pytest.raises(PublicationError): ACL13OneHourAssessmentService().build(acl12,permit,assessment_request,budget,out)
def test_future_authority_denied(assessment_request):
    from src.engine.tooling.strategy_factory.acl_os.acl_13.input_contract import validate_request
    from src.engine.tooling.strategy_factory.acl_os.acl_13.canonical import with_digest
    r=copy.deepcopy(assessment_request); r['known_time_contract']['future_data_allowed']=True; r=with_digest({k:v for k,v in r.items() if k!='assessment_request_digest'},'assessment_request_digest')
    with pytest.raises(ContractError): validate_request(r)
