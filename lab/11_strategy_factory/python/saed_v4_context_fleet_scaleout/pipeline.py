from __future__ import annotations
from copy import deepcopy
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .registry import compile_registry,registry_index
from .isolation import build_isolation_matrix
from .resources import freeze_resource_catalog,freeze_quotas
from .placement import place_fleet
from .manifest import compile_fleet_manifest
from .routing import compile_routes,route_occurrences
from .rollout import freeze_rollout_policy,simulate_rollout
from .health import evaluate_health
from .control_plane import build_control_plane_journal
from .observability import build_observability
from .reconciliation import reconcile
from .chaos import run_chaos_drills
from .governance import review_bundle,evidence_bundle
from .release import qualify_release,certificate,handoff

def run_reference(f:dict)->dict:
 up=verify_upstream(f["upstream_certificate"],f["upstream_handoff"])
 const=freeze_constitution(f["constitution"]);auth=authority_boundary();reg=compile_registry(f["registry"]);idx=registry_index(reg);iso=build_isolation_matrix(reg)
 cat=freeze_resource_catalog(f["resource_catalog"]);quo=freeze_quotas(f["quotas"],reg);pl=place_fleet(reg,cat,quo);man=compile_fleet_manifest(reg,pl,up)
 routes=compile_routes(f["routing_table"],reg,man);route_ledger=route_occurrences(f["occurrences"],routes,reg)
 policy=freeze_rollout_policy(f["rollout_policy"]);health=evaluate_health(f["health_samples"],reg,f["cutoff_time"]);roll=simulate_rollout(reg,policy,f["health_samples"])
 journal=build_control_plane_journal(man,roll,f["commands"]);obs=build_observability(reg,pl,health,routes,roll,journal);rec=reconcile(reg,man,pl,routes,health);chaos=run_chaos_drills(reg,pl);reviews=review_bundle(f["reviews"])
 artifacts={"upstream":up,"constitution":const,"authority":auth,"registry":reg,"registry_index":idx,"isolation":iso,"resources":cat,"quotas":quo,"placement":pl,"manifest":man,"routes":routes,"route_ledger":route_ledger,"rollout_policy":policy,"health":health,"rollout":roll,"control_journal":journal,"observability":obs,"reconciliation":rec,"chaos":chaos}
 evidence=evidence_bundle(artifacts,reviews);release=qualify_release(reg,pl,roll,rec,chaos,obs,evidence);cert=certificate(release,evidence);ho=handoff(cert)
 return {**artifacts,"review_bundle":reviews,"evidence_bundle":evidence,"release":release,"certificate":cert,"handoff":ho}
