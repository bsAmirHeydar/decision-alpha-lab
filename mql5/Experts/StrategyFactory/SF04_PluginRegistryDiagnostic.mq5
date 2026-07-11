#property strict
#property version "1.00"
#property description "Phase 04 static plugin-registry diagnostic"
#include <AlphaLab\StrategyFactory\Plugins\SF04_AllPlugins.mqh>
input string InpSymbol="EURUSD";input ENUM_TIMEFRAMES InpTimeframe=PERIOD_M1;input int InpLookbackBars=64;input int InpTicksPerEvent=25;
int OnInit(){CSF04FixturePulseFactory f;f.Configure(InpSymbol,PeriodSeconds(InpTimeframe),InpLookbackBars,InpTicksPerEvent);CSF04PluginRegistry r;string e="";if(!r.RegisterFactory(&f,e)||!r.ValidateAll(e)){Print("SF04 registry failed: ",e);return INIT_FAILED;}for(int i=0;i<r.Count();i++){SF04_PluginDescriptor d;if(r.DescriptorAt(i,d))Print("plugin[",i,"] id=",d.plugin_id," version=",d.version," kind=",SF04_PluginKindToString(d.kind)," capabilities=",(long)d.capability_mask," update_scope=",d.update_scope_mask," hash=",SF04_PluginDescriptorHash(d));}return INIT_SUCCEEDED;}
