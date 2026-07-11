#ifndef __SF01_CONTRACT_REGISTRY_MQH__
#define __SF01_CONTRACT_REGISTRY_MQH__

#include "SF01_SchemaIdentity.mqh"


SF01_SchemaIdentity SF01_BarRecordSchema()
{
   return SF01_MakeSchemaIdentity("alpha_lab.strategy_factory", "bar_record", 1, 0, 0);
}

SF01_SchemaIdentity SF01_AnatomyEventSchema()
{
   return SF01_MakeSchemaIdentity("alpha_lab.strategy_factory", "anatomy_event", 1, 0, 0);
}

SF01_SchemaIdentity SF01_FeatureValueSchema()
{
   return SF01_MakeSchemaIdentity("alpha_lab.strategy_factory", "feature_value", 1, 0, 0);
}

SF01_SchemaIdentity SF01_FeatureSnapshotSchema()
{
   return SF01_MakeSchemaIdentity("alpha_lab.strategy_factory", "feature_snapshot", 1, 0, 0);
}

SF01_SchemaIdentity SF01_ArtifactIdentitySchema()
{
   return SF01_MakeSchemaIdentity("alpha_lab.strategy_factory", "artifact_identity", 1, 0, 0);
}

#endif
