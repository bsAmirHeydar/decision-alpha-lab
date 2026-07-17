#ifndef SAED_V4_38_COMPILED_RUNTIME_MQH
#define SAED_V4_38_COMPILED_RUNTIME_MQH
// SAED_V4_38 research-only immutable generated runtime.
#define SAED_V4_38_BUNDLE_HASH "95b81258450a1c00de2efba48ebbda68a7363ceb8b5212a26d0af2ad923a8294"
#define SAED_V4_38_POLICY_HASH "7eb3aad47d0643ccaa5a6b61d8d6f249f622c1bc0b91a8f6b2db2a4c2f514c2c"
#define SAED_V4_38_MODEL_HASH "b8a93ad20c73b567cbb5b34000dcc66232aa2223296830a1c35fc8cd6d3cce63"
#define SAED_V4_38_FEATURE_COUNT 12
#define SAED_V4_38_ORDER_SUBMISSION_ALLOWED 0
#define SAED_V4_38_CAPITAL_ACTIVATION_ALLOWED 0
enum SAEDV438FeatureIndex {
   SAEDV438_FEATURE_PRICE_RETURN_1 = 0,
   SAEDV438_FEATURE_VOLATILITY_20 = 1,
   SAEDV438_FEATURE_SPREAD_BPS = 2,
   SAEDV438_FEATURE_LIQUIDITY_RATIO = 3,
   SAEDV438_FEATURE_CONTEXT_SCORE = 4,
   SAEDV438_FEATURE_TREATMENT_SCORE = 5,
   SAEDV438_FEATURE_EXPECTED_EDGE_BPS = 6,
   SAEDV438_FEATURE_EXPECTED_COST_BPS = 7,
   SAEDV438_FEATURE_PORTFOLIO_RISK = 8,
   SAEDV438_FEATURE_SESSION_PROGRESS = 9,
   SAEDV438_FEATURE_DRAWDOWN_STATE = 10,
   SAEDV438_FEATURE_OOD_SCORE = 11
};
static const double SAEDV438Weights[12]={
   0.25,
   -0.15,
   -0.005,
   0.012,
   0.02,
   -0.35,
   -0.2,
   0.08,
   0.04,
   -0.01,
   0.28,
   -0.1
};
static const double SAEDV438Bias=0.18;
double SAEDV438Quantize(const double x){return MathRound(x*100000000.0)/100000000.0;}
double SAEDV438LinearScore(const double &features[]){double s=SAEDV438Bias; for(int i=0;i<12;i++) s+=SAEDV438Weights[i]*features[i]; return SAEDV438Quantize(s);}
bool SAEDV438Evaluate(const double &f[],string &decision,string &treatment,double &confidence,double &net_edge,double &size_fraction){
 if(ArraySize(f)!=12){decision="ABSTAIN";treatment="BASELINE";confidence=0;net_edge=0;size_fraction=0;return false;}
 const double model_score=SAEDV438LinearScore(f);
 net_edge=SAEDV438Quantize(f[6]-f[7]);
 const bool allowed=(f[11]<=0.20 && f[8]<=0.80 && net_edge>=3.0 && f[9]>=0.05 && f[9]<=0.95 && f[10]<=0.70 && model_score>=0.55);
 if(!allowed){decision="ABSTAIN";treatment="BASELINE";confidence=0;size_fraction=0;return false;}
 decision="SELECT";treatment="TRT_RUNTIME_REFERENCE";confidence=SAEDV438Quantize(MathMax(0.0,MathMin(1.0,model_score)));size_fraction=SAEDV438Quantize(confidence*0.25);return true;
}
#endif
