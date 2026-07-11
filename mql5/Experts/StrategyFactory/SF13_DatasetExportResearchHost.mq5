#property strict
#include <AlphaLab/StrategyFactory/Training/SF13_AllTraining.mqh>
input bool InpExportReferenceDataset=false;
int OnInit(){if(!InpExportReferenceDataset){Print("SF13 dataset export host initialized in no-write diagnostic mode");return INIT_SUCCEEDED;}Print("SF13 export requires upstream immutable rows and remains research-only");return INIT_SUCCEEDED;}void OnTick(){}
