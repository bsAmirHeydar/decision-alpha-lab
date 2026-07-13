#ifndef __EXP0019_FP_I04_CURSOR_MQH__
#define __EXP0019_FP_I04_CURSOR_MQH__
#include "FP_I04_Revision.mqh"
void FP_I04_EmptyCursor(const string pair_id,FP_I04_IncrementalCursor &c){c.pair_id=pair_id;c.last_emitted_open_utc=0;c.left_last_source_sequence=-1;c.right_last_source_sequence=-1;c.data_revision_id="NONE";c.state=FP_I04_CURSOR_EMPTY;c.cursor_id=FP_I02_CompactId("FPCURSOR",pair_id+"|EMPTY");}
bool FP_I04_ValidateResume(const FP_I04_IncrementalCursor &c,const string parent,string &reason){if(c.state==FP_I04_CURSOR_INVALIDATED){reason="FP_DRC_CURSOR_INVALIDATED";return false;}if(c.data_revision_id!="NONE"&&c.data_revision_id!=parent){reason="FP_DRC_CURSOR_REVISION_MISMATCH";return false;}reason="FP_DRC_CURSOR_VALID";return true;}
#endif
