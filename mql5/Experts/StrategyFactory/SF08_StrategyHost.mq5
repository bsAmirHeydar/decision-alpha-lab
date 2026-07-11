#property strict
#property version "1.00"
#property description "Strategy Factory Phase 08 central candidate host without legacy strategy integration"
#include <AlphaLab\StrategyFactory\Candidate\SF08_AllCandidate.mqh>
input int InpCandidateQueueCapacity=64;
CSF08PolicyRegistry g_registry;CSF08FixturePolicyPack g_pack;CSF08CandidateMatrixPlan g_matrix;CSF08CandidateEngine g_engine;
int OnInit(){string e="";if(!g_pack.RegisterAll(g_registry,e)||!g_registry.Compile(e)||!g_pack.BuildReferenceMatrix(g_matrix,e)||!g_matrix.Compile(g_registry,e)||!g_engine.Initialize(&g_registry,&g_matrix,InpCandidateQueueCapacity,SF08_QUEUE_FAIL_ENGINE,e)){Print("SF08 host initialization failed: ",e);return INIT_FAILED;}Print("SF08 central candidate host ready. No legacy strategy and no order authority. registry=",g_registry.RegistryHash()," matrix=",g_matrix.PlanHash());return INIT_SUCCEEDED;}
