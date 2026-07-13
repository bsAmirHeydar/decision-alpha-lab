from .contracts import AdvancedAlgorithmDescriptor
from .enums import AdvancedTaskFamily

def d(i,f,form,tasks,fields,outputs,native=True,dep='',params=None,limits=(),exports=('native_json',)):
 return AdvancedAlgorithmDescriptor(i,'1.0.0',f,form,tuple(tasks),native,'bit_exact' if native else 'numeric_tolerance',tuple(fields),tuple(outputs),tuple(exports),dep,params or {},tuple(limits))
CATALOG=(
 d('pairwise_linear_ranker',AdvancedTaskFamily.RANKING,'pairwise',('ranking',),('ranking_group','utility'),('rank_score',),params={'epochs':240,'learning_rate':.04,'l2':.001}),
 d('listwise_softmax_ranker',AdvancedTaskFamily.RANKING,'listwise',('ranking',),('ranking_group','utility'),('rank_score',),False,'lightgbm',limits=('optional dependency','group ordering required')),
 d('lambdamart_ranker',AdvancedTaskFamily.RANKING,'lambda_rank',('ranking',),('ranking_group','utility'),('rank_score',),False,'lightgbm',limits=('optional dependency','portfolio top-k validation mandatory')),
 d('direct_outcome_selector',AdvancedTaskFamily.TREATMENT_SELECTION,'direct_outcome',('treatment_choice',),('treatment_id','utility','action_mask'),('utility_by_action','chosen_action'),params={'minimum_support':5,'alpha':.01}),
 d('one_vs_rest_utility_selector',AdvancedTaskFamily.TREATMENT_SELECTION,'one_vs_rest',('treatment_choice',),('treatment_id','utility','action_mask'),('utility_by_action','chosen_action')),
 d('doubly_robust_selector',AdvancedTaskFamily.TREATMENT_SELECTION,'doubly_robust',('treatment_choice','bounded_policy'),('logged_action','propensity','outcome_model','action_mask'),('policy_value','standard_error'),limits=('requires overlap and propensity audit',)),
 d('kaplan_meier',AdvancedTaskFamily.SURVIVAL,'nonparametric',('survival',),('duration','event'),('survival_curve',)),
 d('discrete_hazard',AdvancedTaskFamily.SURVIVAL,'discrete_time',('survival','competing_risk'),('duration','event','cause'),('survival_curve','cause_cif'),params={'alpha':1.0}),
 d('cox_proportional_hazards',AdvancedTaskFamily.SURVIVAL,'cox',('survival',),('duration','event'),('risk_score','survival_curve'),False,'lifelines',limits=('proportional hazards assumption must be audited',)),
 d('aft_weibull',AdvancedTaskFamily.SURVIVAL,'aft',('survival',),('duration','event'),('time_quantiles',),False,'lifelines'),
 d('random_survival_forest',AdvancedTaskFamily.SURVIVAL,'survival_forest',('survival','competing_risk'),('duration','event','cause'),('survival_curve',),False,'scikit-survival'),
 d('empirical_quantiles',AdvancedTaskFamily.DISTRIBUTIONAL,'empirical',('quantile',),('utility',),('quantiles',)),
 d('linear_quantile_regression',AdvancedTaskFamily.DISTRIBUTIONAL,'pinball',('quantile',),('utility',),('quantiles',),False,'scikit-learn'),
 d('conformal_residual_interval',AdvancedTaskFamily.DISTRIBUTIONAL,'split_conformal',('quantile','regression'),('calibration_residuals',),('lower','upper')),
 d('distributional_boosting',AdvancedTaskFamily.DISTRIBUTIONAL,'distributional_boosting',('quantile',),('utility',),('distribution_parameters','quantiles'),False,'lightgbm'),
 d('shared_linear_heads',AdvancedTaskFamily.MULTI_TASK,'hard_parameter_sharing',('multi_task',),('multi_output_target',),('head_outputs',),params={'alpha':.01}),
 d('regime_centroid_gate',AdvancedTaskFamily.REGIME_GATING,'mixture_of_experts',('regime_gating',),('regime_label','features'),('expert_key','fallback'),params={'minimum_support':10}),
 d('conservative_policy_improvement',AdvancedTaskFamily.BOUNDED_POLICY,'offline_cpi',('bounded_policy',),('logged_action','reward','propensity','action_mask'),('action','abstention','improvement_lcb'),limits=('cannot generate unseen actions','requires overlap audit')),
)
BY_KEY={x.key:x for x in CATALOG};BY_FAMILY={f:tuple(x for x in CATALOG if x.family is f) for f in AdvancedTaskFamily}
