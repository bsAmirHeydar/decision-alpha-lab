from .contracts import AlgorithmDescriptor,DependencyRequirement
from .enums import *
SK=DependencyRequirement('sklearn','scikit-learn','>=1.4',DependencyMode.REQUIRED,'classical tabular estimators')
XGB=DependencyRequirement('xgboost','xgboost','>=2.0',DependencyMode.OPTIONAL,'gradient boosted trees')
LGB=DependencyRequirement('lightgbm','lightgbm','>=4.0',DependencyMode.OPTIONAL,'gradient boosted trees')
CAT=DependencyRequirement('catboost','catboost','>=1.2',DependencyMode.OPTIONAL,'ordered boosting')
def d(i,f,tasks=('binary_classification',),prob=True,dep=(),default=None,bounded=None,portable=PortabilityLevel.PARAMETER_SNAPSHOT,exports=('native_json',),tags=(),limits=(),weights=True,multi=False,missing=False):
 return AlgorithmDescriptor(i,'1.0.0',f,f'uce.classical.{i}','1.0.0',tuple(tasks),prob,weights,missing,multi,'numeric_tolerance',portable,tuple(exports),tuple(dep),default or {},bounded or {},tuple(tags),tuple(limits))
def build_catalog():
 return (
 d('never_trade',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,tags=('naive','mandatory')),
 d('always_trade',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,tags=('naive','mandatory')),
 d('prevalence',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,tags=('naive','mandatory')),
 d('manual_threshold',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,default={'feature_index':0,'threshold':0.0,'direction':1},tags=('manual','mandatory')),
 d('single_feature_search',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,default={'max_thresholds':64},tags=('transparent','mandatory')),
 d('rate_matched_null',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,tags=('null','mandatory')),
 d('random_null',AlgorithmFamily.BASELINE,portable=PortabilityLevel.NATIVE_JSON,tags=('null',)),
 d('linear_regression',AlgorithmFamily.LINEAR,('regression',),False,(SK,),{'fit_intercept':True},tags=('linear','mandatory')),
 d('ridge_regression',AlgorithmFamily.LINEAR,('regression',),False,(SK,),{'alpha':1.0},bounded={'alpha':(0.0001,10000.0)},tags=('linear','mandatory')),
 d('lasso_regression',AlgorithmFamily.LINEAR,('regression',),False,(SK,),{'alpha':0.01,'max_iter':5000},bounded={'alpha':(0.000001,100.0)},tags=('sparse',)),
 d('elastic_net',AlgorithmFamily.LINEAR,('regression',),False,(SK,),{'alpha':0.01,'l1_ratio':0.5,'max_iter':5000},bounded={'alpha':(0.000001,100.0),'l1_ratio':(0.0,1.0)},tags=('sparse',)),
 d('huber_regression',AlgorithmFamily.LINEAR,('regression',),False,(SK,),{'epsilon':1.35,'alpha':0.0001},tags=('robust',)),
 d('logistic_regression',AlgorithmFamily.LINEAR,('binary_classification','multiclass_classification'),True,(SK,),{'C':1.0,'max_iter':2000,'solver':'lbfgs'},bounded={'C':(0.0001,10000.0)},exports=('native_json','onnx','mql5_linear'),tags=('linear','mandatory','calibratable'),multi=True),
 d('ridge_classifier',AlgorithmFamily.LINEAR,('binary_classification','multiclass_classification'),False,(SK,),{'alpha':1.0},tags=('linear',),multi=True),
 d('linear_svm',AlgorithmFamily.KERNEL,('binary_classification','multiclass_classification'),False,(SK,),{'C':1.0,'max_iter':10000},tags=('margin',),multi=True),
 d('rbf_svm',AlgorithmFamily.KERNEL,('binary_classification','multiclass_classification'),True,(SK,),{'C':1.0,'gamma':'scale','probability':True},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('kernel','compute_gated'),multi=True),
 d('knn_classifier',AlgorithmFamily.NEIGHBORHOOD,('binary_classification','multiclass_classification'),True,(SK,),{'n_neighbors':7,'weights':'distance'},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('distance',),multi=True),
 d('knn_regressor',AlgorithmFamily.NEIGHBORHOOD,('regression',),False,(SK,),{'n_neighbors':7,'weights':'distance'},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('distance',)),
 d('nearest_centroid',AlgorithmFamily.NEIGHBORHOOD,('binary_classification','multiclass_classification'),False,(SK,),{},tags=('distance','transparent'),multi=True),
 d('decision_tree_classifier',AlgorithmFamily.TREE,('binary_classification','multiclass_classification'),True,(SK,),{'max_depth':4,'min_samples_leaf':2},tags=('tree','mandatory'),multi=True),
 d('decision_tree_regressor',AlgorithmFamily.TREE,('regression',),False,(SK,),{'max_depth':4,'min_samples_leaf':2},tags=('tree','mandatory')),
 d('random_forest_classifier',AlgorithmFamily.TREE,('binary_classification','multiclass_classification'),True,(SK,),{'n_estimators':64,'max_depth':8,'min_samples_leaf':2,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('ensemble','mandatory'),multi=True),
 d('random_forest_regressor',AlgorithmFamily.TREE,('regression',),False,(SK,),{'n_estimators':64,'max_depth':8,'min_samples_leaf':2,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('ensemble','mandatory')),
 d('extra_trees_classifier',AlgorithmFamily.TREE,('binary_classification','multiclass_classification'),True,(SK,),{'n_estimators':64,'max_depth':8,'min_samples_leaf':2,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('ensemble',),multi=True),
 d('extra_trees_regressor',AlgorithmFamily.TREE,('regression',),False,(SK,),{'n_estimators':64,'max_depth':8,'min_samples_leaf':2,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('ensemble',)),
 d('gradient_boosting_classifier',AlgorithmFamily.BOOSTING,('binary_classification','multiclass_classification'),True,(SK,),{'n_estimators':64,'learning_rate':0.05,'max_depth':3},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('boosting',),multi=True),
 d('gradient_boosting_regressor',AlgorithmFamily.BOOSTING,('regression',),False,(SK,),{'n_estimators':64,'learning_rate':0.05,'max_depth':3,'loss':'huber'},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('boosting',)),
 d('hist_gradient_boosting_classifier',AlgorithmFamily.BOOSTING,('binary_classification','multiclass_classification'),True,(SK,),{'max_iter':80,'learning_rate':0.05,'max_leaf_nodes':31},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('boosting','histogram'),multi=True,missing=True),
 d('hist_gradient_boosting_regressor',AlgorithmFamily.BOOSTING,('regression',),False,(SK,),{'max_iter':80,'learning_rate':0.05,'max_leaf_nodes':31},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('boosting','histogram'),missing=True),
 d('gaussian_nb',AlgorithmFamily.PROBABILISTIC,('binary_classification','multiclass_classification'),True,(SK,),{'var_smoothing':1e-9},tags=('bayesian','calibratable'),multi=True),
 d('bernoulli_nb',AlgorithmFamily.PROBABILISTIC,('binary_classification','multiclass_classification'),True,(SK,),{'alpha':1.0,'binarize':0.0},tags=('bayesian',),multi=True),
 d('multinomial_nb',AlgorithmFamily.PROBABILISTIC,('binary_classification','multiclass_classification'),True,(SK,),{'alpha':1.0},tags=('bayesian','nonnegative_features'),multi=True),
 d('spline_logistic_gam',AlgorithmFamily.ADDITIVE,('binary_classification',),True,(SK,),{'n_knots':5,'degree':3,'C':1.0},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('gam','additive','interpretable')),
 d('spline_ridge_gam',AlgorithmFamily.ADDITIVE,('regression',),False,(SK,),{'n_knots':5,'degree':3,'alpha':1.0},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('gam','additive','interpretable')),
 d('xgboost_classifier',AlgorithmFamily.OPTIONAL_EXTERNAL,('binary_classification','multiclass_classification'),True,(XGB,),{'n_estimators':64,'max_depth':4,'learning_rate':0.05,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,exports=('native_json','onnx'),tags=('optional','boosting'),multi=True),
 d('xgboost_regressor',AlgorithmFamily.OPTIONAL_EXTERNAL,('regression',),False,(XGB,),{'n_estimators':64,'max_depth':4,'learning_rate':0.05,'n_jobs':1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,exports=('native_json','onnx'),tags=('optional','boosting')),
 d('lightgbm_classifier',AlgorithmFamily.OPTIONAL_EXTERNAL,('binary_classification','multiclass_classification'),True,(LGB,),{'n_estimators':64,'num_leaves':31,'learning_rate':0.05,'n_jobs':1,'verbosity':-1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('optional','boosting'),multi=True),
 d('lightgbm_regressor',AlgorithmFamily.OPTIONAL_EXTERNAL,('regression',),False,(LGB,),{'n_estimators':64,'num_leaves':31,'learning_rate':0.05,'n_jobs':1,'verbosity':-1},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('optional','boosting')),
 d('catboost_classifier',AlgorithmFamily.OPTIONAL_EXTERNAL,('binary_classification','multiclass_classification'),True,(CAT,),{'iterations':64,'depth':5,'learning_rate':0.05,'thread_count':1,'verbose':False},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('optional','boosting'),multi=True),
 d('catboost_regressor',AlgorithmFamily.OPTIONAL_EXTERNAL,('regression',),False,(CAT,),{'iterations':64,'depth':5,'learning_rate':0.05,'thread_count':1,'verbose':False},portable=PortabilityLevel.LIBRARY_ARTIFACT_REQUIRED,tags=('optional','boosting')),
 )
CATALOG=build_catalog();BY_ID={x.algorithm_id:x for x in CATALOG}
