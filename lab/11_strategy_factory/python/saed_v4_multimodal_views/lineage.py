from .canonical import merkle_root,content_hash
def feature_lineage_root(source_values):
    leaves=[]
    for value in source_values:
        leaves.append(content_hash({'source_artifact_id':value.source_artifact_id,'source_hash':value.source_hash,'value_hash':value.value_hash,'lineage_ids':sorted(value.lineage_ids)}))
    return merkle_root(sorted(leaves))
def view_lineage_root(features):
    leaves=[]
    for f in features:
        leaves.extend(f.source_value_hashes);leaves.extend(f.source_artifact_ids)
    return merkle_root(sorted(set(leaves)))
def package_lineage_root(views):return merkle_root(sorted(v.lineage_root for v in views))
