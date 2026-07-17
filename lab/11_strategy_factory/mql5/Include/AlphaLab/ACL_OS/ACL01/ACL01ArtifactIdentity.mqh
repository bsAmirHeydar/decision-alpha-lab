#ifndef ALPHALAB_ACL01_ARTIFACT_IDENTITY_MQH
#define ALPHALAB_ACL01_ARTIFACT_IDENTITY_MQH
struct ACL01ArtifactIdentity { string artifact_id; string tenant_id; string name_space; string kind; string name; string version; string sha256_digest; };
bool ACL01IdentityIsStructurallyValid(const ACL01ArtifactIdentity &x) { return StringLen(x.artifact_id)>0 && StringFind(x.artifact_id,"al://")==0 && StringLen(x.version)>0 && StringFind(x.sha256_digest,"sha256:")==0; }
#endif
