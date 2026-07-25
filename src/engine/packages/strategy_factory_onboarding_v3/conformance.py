from __future__ import annotations
from .contracts import ContextSpecification,ScaffoldManifest,CompiledTournamentTemplate,EngineInvarianceReport
from .enums import InvarianceStatus
from .errors import OnboardingError
def assert_conformant(spec:ContextSpecification,manifest:ScaffoldManifest,compiled:CompiledTournamentTemplate,invariance:EngineInvarianceReport)->None:
    if manifest.context_spec_hash!=spec.spec_hash:raise OnboardingError('spec_manifest_mismatch','manifest spec mismatch')
    if manifest.tournament_template_hash!=compiled.compiled_hash:raise OnboardingError('template_manifest_mismatch','compiled tournament mismatch')
    if invariance.status is not InvarianceStatus.PASS:raise OnboardingError('core_invariance_failed','central engine changed')
    required={'schema','fixture','test','documentation','contract'}
    actual={a.kind for a in manifest.artifacts}
    if not required<=actual:raise OnboardingError('incomplete_scaffold','scaffold missing artifact families',{'missing':sorted(required-actual)})
