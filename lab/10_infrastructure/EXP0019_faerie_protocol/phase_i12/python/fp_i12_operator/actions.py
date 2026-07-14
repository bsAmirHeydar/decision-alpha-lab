from dataclasses import replace
from .contracts import *
from .preferences import normalize_preferences,set_filters,set_panel
from .errors import FPI12Error

def apply_action(request,prefs):
 p=prefs;export=False;rebuild=False;disp=ActionDisposition.APPLIED;reason='FP_UX_ACTION_APPLIED'
 try:
  if request.action is OperatorAction.TOGGLE_PANEL:
   nxt=PanelState.COLLAPSED if p.panel.state is PanelState.EXPANDED else PanelState.EXPANDED;p=set_panel(p,replace(p.panel,state=nxt))
  elif request.action is OperatorAction.SET_MODE:p=set_panel(p,replace(p.panel,mode=PanelMode(request.value)))
  elif request.action is OperatorAction.SET_PAGE:p=normalize_preferences(replace(p,page=max(0,int(request.value))))
  elif request.action is OperatorAction.NEXT_PAGE:p=normalize_preferences(replace(p,page=p.page+1))
  elif request.action is OperatorAction.PREVIOUS_PAGE:p=normalize_preferences(replace(p,page=max(0,p.page-1)))
  elif request.action is OperatorAction.FOCUS_SEMANTIC_ID:p=set_filters(p,replace(p.filters,focus_semantic_id=request.value))
  elif request.action is OperatorAction.RESET_FILTERS:p=set_filters(p,FilterConfig())
  elif request.action is OperatorAction.EXPORT_SNAPSHOT:export=True;disp=ActionDisposition.REQUEST_RECORDED;reason='FP_EXPORT_REQUEST_RECORDED'
  elif request.action is OperatorAction.REQUEST_REBUILD:rebuild=True;disp=ActionDisposition.REQUEST_RECORDED;reason='FP_REBUILD_REQUEST_RECORDED'
  elif request.action in (OperatorAction.ACK_ALERT,OperatorAction.ACK_ALL):disp=ActionDisposition.REQUEST_RECORDED;reason='FP_ALERT_ACK_REQUEST_RECORDED'
  else:disp=ActionDisposition.NOOP;reason='FP_UX_ACTION_NOOP'
 except (ValueError,FPI12Error):disp=ActionDisposition.REJECTED;reason='FP_UX_ACTION_INVALID';p=prefs
 return ActionResult(request.action_id,disp,reason,p,rebuild,export)
