#pragma once
bool SAEDV413CheckpointIsReferenceOnly(const bool production_eligible,const bool runtime_authority){ return !production_eligible && !runtime_authority; }
