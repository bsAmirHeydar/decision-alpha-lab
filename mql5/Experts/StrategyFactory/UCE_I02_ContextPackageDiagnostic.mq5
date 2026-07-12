#property strict
#property version   "1.00"
#property description "UCEE I02 context package SDK diagnostic. No order authority."
#include <AlphaLab/StrategyFactory/ContextPackage/UCE02_All.mqh>
input bool InpUseEXP0017Reference=false;
int OnInit()
{
   UCE02_ConformanceTelemetry telemetry;UCE02_ResetConformanceTelemetry(telemetry);string error="";
   IUCE02ContextPackage *package=NULL;
   if(InpUseEXP0017Reference)package=new CUCE02EXP0017ReferencePackage();
   else package=new CUCE02SyntheticBreakPackage();
   if(CheckPointer(package)==POINTER_INVALID){Print("UCE-I02 allocation failure");return INIT_FAILED;}
   UCE02_ContextPackageManifest manifest;package.GetManifest(manifest);
   const bool ok=UCE02_LintPackage(package,telemetry,error);
   PrintFormat("UCE-I02 package=%s version=%s identity=%s features=%d views=%d clusters=%d status=%s error=%s",
               manifest.package_id,manifest.version,UCE02_PackageIdentity(manifest),package.FeatureCount(),package.ViewCount(),package.ClusterRuleCount(),ok?"PASS":"FAIL",error);
   delete package;
   return ok?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
