#ifndef __UCEI04_MANUAL_MQH__
#define __UCEI04_MANUAL_MQH__
#include "UCEI04_Matrix.mqh"
struct UCEI04_ManualBundle{string bundle_id;string version;string owner_id;UCEI04_TreatmentDraft draft;string expected_treatment_id;bool frozen;string definition_id;};
class CUCEI04ManualCompiler{
public:
 bool Compile(UCEI04_ManualBundle &b,const UCEI03_BuildContext &c,CUCEI03Catalog &catalog,CUCEI04TreatmentCompiler &compiler,UCEI04_CompiledTreatment &t,string &error){if(!b.frozen){error="bundle_not_frozen";return false;}if(!b.draft.pinned){error="draft_not_pinned";return false;}if(!compiler.Compile(b.draft,c,catalog,t,error))return false;if(b.expected_treatment_id!=""&&b.expected_treatment_id!=t.treatment_id){error="manual_parity_mismatch";return false;}error="";return true;}
};
#endif
