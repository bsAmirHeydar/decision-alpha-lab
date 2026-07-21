from __future__ import annotations
from collections import defaultdict
import re
from pathlib import Path, PurePosixPath
from .canonical import digest_object, stable_id
from .constants import REFERENCE_SCAN_EXTENSIONS, EXCLUDED_PARTS, SELF_EXCLUDED_PREFIXES, SELF_EXCLUDED_ROOT_PREFIXES
from .frontmatter import heading_anchors

_MD_LINK=re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_WIKI_LINK=re.compile(r"\[\[([^\]]+)\]\]")
_RAW_PATH=re.compile(r"(?<![A-Za-z0-9_])((?:docs|lab|registry|mql5|tools)/[A-Za-z0-9_./()\- ]+\.(?:md|mdx|rst|txt|adoc)|(?:README|INSTALL|ROLLBACK|COMMIT_MESSAGE|LCM|ACL_OS|SAED|NDS)[A-Za-z0-9_.\- ]*\.md)")

def _excluded(rel,parts):
    if any(x in EXCLUDED_PARTS for x in parts):return True
    if any(rel.startswith(x) for x in SELF_EXCLUDED_PREFIXES):return True
    return any(parts[-1].startswith(x) for x in SELF_EXCLUDED_ROOT_PREFIXES) if parts else False

def _clean_target(value):
    value=value.strip().strip("<>").replace(chr(92),"/")
    if value.startswith(("http://","https://","mailto:","data:","#")):return None,None,True
    if " " in value and not value.startswith("./") and not value.startswith("../"):
        first=value.split()[0]
        if first.endswith(tuple(REFERENCE_SCAN_EXTENSIONS)):value=first
    path,anchor=(value.split("#",1)+[None])[:2] if "#" in value else (value,None)
    return path.strip(),anchor.strip().lower() if anchor else None,False

def build_reference_graph(repo_root:Path,documents):
    by_path={row["path"]:row for row in documents};basename=defaultdict(list)
    for row in documents:basename[Path(row["path"]).stem.lower()].append(row["path"])
    edges=[];unresolved=[];external_count=0;source_file_count=0
    for source in sorted(repo_root.rglob("*"),key=lambda p:p.as_posix().lower()):
        if not source.is_file() or source.suffix.lower() not in REFERENCE_SCAN_EXTENSIONS:continue
        rel=source.relative_to(repo_root).as_posix()
        if _excluded(rel,source.relative_to(repo_root).parts):continue
        if source.stat().st_size>2_000_000:continue
        text=source.read_text(encoding="utf-8",errors="replace");source_file_count+=1
        refs=[]
        for match in _MD_LINK.finditer(text):refs.append(("MARKDOWN",match.group(1)))
        for match in _WIKI_LINK.finditer(text):refs.append(("WIKI",match.group(1)))
        for match in _RAW_PATH.finditer(text):refs.append(("RAW_PATH",match.group(1)))
        seen=set()
        for kind,raw in refs:
            key=(kind,raw)
            if key in seen:continue
            seen.add(key)
            if kind=="WIKI":
                value=raw.split("|",1)[0];path_part,anchor=(value.split("#",1)+[None])[:2] if "#" in value else (value,None)
                candidate=path_part.strip().replace(chr(92),"/")
                if candidate.lower().endswith(tuple(REFERENCE_SCAN_EXTENSIONS)):
                    candidate=candidate.rsplit(".",1)[0]
                matches=basename.get(Path(candidate).name.lower(),[])
                if len(matches)==1:target=matches[0];resolution="UNIQUE_BASENAME"
                elif len(matches)>1:
                    unresolved.append({"unknown_id":stable_id("DOCREFAMB",rel,raw),"unknown_type":"AMBIGUOUS_WIKI_LINK","source_path":rel,"raw_target":raw,"candidate_paths":sorted(matches),"blocking_scope":"SOURCE_PATH","validation_status":"UNKNOWN"});continue
                else:
                    unresolved.append({"unknown_id":stable_id("DOCREFMISS",rel,raw),"unknown_type":"UNRESOLVED_WIKI_LINK","source_path":rel,"raw_target":raw,"candidate_paths":[],"blocking_scope":"SOURCE_PATH","validation_status":"UNKNOWN"});continue
                anchor=anchor.lower() if anchor else None;is_external=False
            else:
                candidate,anchor,is_external=_clean_target(raw)
                if is_external:external_count+=1;continue
                if not candidate:continue
                base=PurePosixPath(rel).parent
                if candidate.startswith("/"):target=candidate.lstrip("/")
                elif candidate.startswith(("docs/","lab/","registry/","mql5/","tools/")) or candidate in by_path:target=candidate
                else:target=str((base/PurePosixPath(candidate))).replace(chr(92),"/")
                parts=[]
                for part in PurePosixPath(target).parts:
                    if part=="..":
                        if parts:parts.pop()
                    elif part not in (".",""):parts.append(part)
                target="/".join(parts)
                if target not in by_path:
                    unresolved.append({"unknown_id":stable_id("DOCREFMISS",rel,raw),"unknown_type":"UNRESOLVED_DOCUMENT_REFERENCE","source_path":rel,"raw_target":raw,"resolved_candidate":target,"candidate_paths":[],"blocking_scope":"SOURCE_PATH","validation_status":"UNKNOWN"});continue
                resolution="ROOT_OR_RELATIVE_PATH"
            anchor_status="NOT_APPLICABLE"
            if anchor:
                anchors=set(by_path[target].get("heading_anchors",[]))
                anchor_status="PASS" if anchor in anchors else "UNKNOWN"
                if anchor_status!="PASS":
                    unresolved.append({"unknown_id":stable_id("DOCANCHOR",rel,target,anchor),"unknown_type":"UNRESOLVED_HEADING_ANCHOR","source_path":rel,"target_path":target,"anchor":anchor,"candidate_paths":[],"blocking_scope":"EDGE","validation_status":"UNKNOWN"})
            edge={"edge_id":stable_id("DOCREF",rel,target,anchor or ""),"source_path":rel,"target_document_id":by_path[target]["document_id"],"target_path":target,"reference_kind":kind,"resolution_method":resolution,"anchor":anchor,"anchor_status":anchor_status,"validation_status":"PASS" if anchor_status in ("PASS","NOT_APPLICABLE") else "UNKNOWN"}
            edge["edge_digest"]=digest_object(edge,"edge_digest");edges.append(edge)
    inbound=defaultdict(int);outbound=defaultdict(int)
    for edge in edges:inbound[edge["target_path"]]+=1;outbound[edge["source_path"]]+=1
    return {"edges":sorted(edges,key=lambda x:(x["source_path"],x["target_path"],x.get("anchor") or "")),"unresolved":sorted(unresolved,key=lambda x:(x.get("source_path",""),x.get("raw_target",x.get("target_path","")))),"inbound_counts":dict(inbound),"outbound_counts":dict(outbound),"external_reference_count":external_count,"source_file_count":source_file_count}
