#ifndef ALPHALAB_ACL05_OBJECT_REFERENCE_MQH
#define ALPHALAB_ACL05_OBJECT_REFERENCE_MQH
#include "ACL05Types.mqh"
bool ACL05DigestShapeValid(const string value){ return StringLen(value)==71 && StringSubstr(value,0,7)=="sha256:"; }
bool ACL05ObjectRefValid(const ACL05ArtifactRef &x){ return StringLen(x.logical_id)>0 && ACL05DigestShapeValid(x.digest) && x.size_bytes>=0 && x.immutable; }
#endif
