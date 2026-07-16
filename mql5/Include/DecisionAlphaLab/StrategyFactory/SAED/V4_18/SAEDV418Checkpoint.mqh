#pragma once
struct SAEDV418Checkpoint { string checkpoint_id; string policy_id; string checkpoint_hash; bool immutable; bool production_authority; };
bool SAEDV418CheckpointSafe(const SAEDV418Checkpoint &x){ return x.immutable && !x.production_authority; }
