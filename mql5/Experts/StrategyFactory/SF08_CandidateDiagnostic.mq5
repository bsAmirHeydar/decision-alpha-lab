#property strict
#property version "1.00"
#property description "Strategy Factory Phase 08 deterministic candidate matrix diagnostic"
#include <AlphaLab\StrategyFactory\Candidate\SF08_AllCandidate.mqh>
int OnInit(){CSF08PolicyRegistry registry;CSF08FixturePolicyPack pack;CSF08CandidateMatrixPlan matrix;string e="";if(!pack.RegisterAll(registry,e)||!registry.Compile(e)||!pack.BuildReferenceMatrix(matrix,e)||!matrix.Compile(registry,e)){Print("SF08 diagnostic failed: ",e);return INIT_FAILED;}Print("SF08 diagnostic ready registry=",registry.RegistryHash()," matrix=",matrix.PlanHash()," templates=",matrix.Count());return INIT_SUCCEEDED;}
