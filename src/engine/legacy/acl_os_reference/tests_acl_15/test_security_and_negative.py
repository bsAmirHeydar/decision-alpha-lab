import copy,pytest
from tools.strategy_factory.acl_os.acl_15.service import ACL15FleetOperationsClosureService
from tools.strategy_factory.acl_os.acl_15.errors import IntegrityError
def test_existing_destination_denied(tmp_path,acl14_root,permit,policy):
 out=tmp_path/'out'; out.mkdir()
 with pytest.raises(IntegrityError): ACL15FleetOperationsClosureService().build(acl14_root,permit,policy,out)
def test_policy_disables_auto_reopen(policy): assert policy['automatic_reopen_allowed'] is False
def test_policy_disables_history_mutation(policy): assert policy['closed_history_mutation_allowed'] is False
def test_policy_not_production_fleet(policy): assert policy['production_fleet_claimed'] is False
