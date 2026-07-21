from .conftest import REPO
def test_delivery_and_atomic_docs_are_comprehensive():
 d=REPO/"docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_10B";a=REPO/"docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/12_ATOMIC_CONCEPTS/LCM_10B";assert len(list(d.glob("*.md")))>=60;assert len(list(a.glob("*.md")))>=30
