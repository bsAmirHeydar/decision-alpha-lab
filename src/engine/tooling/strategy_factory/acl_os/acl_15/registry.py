from __future__ import annotations
from .canonical import with_digest
from .policies import FLEET_STATUSES,CLOSURE_STATES,ALLOWED_REOPEN_ACTIONS,FORBIDDEN_ACTIONS,REPORT_SECTIONS
def build_registries()->dict:
    fleet=with_digest({'schema_version':'1.0.0','registry_id':'ACL15_FLEET_STATUS_REGISTRY_V1','statuses':[{'status_id':x,'version':'1.0.0'} for x in FLEET_STATUSES],'dynamic_registration_allowed':False},'registry_digest')
    closure=with_digest({'schema_version':'1.0.0','registry_id':'ACL15_CLOSURE_STATE_REGISTRY_V1','states':[{'state_id':x,'version':'1.0.0'} for x in CLOSURE_STATES],'dynamic_registration_allowed':False},'registry_digest')
    actions=with_digest({'schema_version':'1.0.0','registry_id':'ACL15_ACTION_REGISTRY_V1','allowed_reopen_actions':ALLOWED_REOPEN_ACTIONS,'forbidden_actions':FORBIDDEN_ACTIONS,'implicit_actions_allowed':False},'registry_digest')
    report=with_digest({'schema_version':'1.0.0','registry_id':'ACL15_REPORT_SECTION_REGISTRY_V1','sections':[{'section_id':x,'required':True,'order':i+1} for i,x in enumerate(REPORT_SECTIONS)],'dynamic_sections_allowed':False},'registry_digest')
    return {'fleet':fleet,'closure':closure,'actions':actions,'report':report}
