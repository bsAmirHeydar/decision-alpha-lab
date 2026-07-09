# Release Profile Contract

A release profile is not decoration. It controls whether the build is a development surface, a beta test build, a stable customer package, or an internal support build.

## Inputs

- `InpProductVersion`
- `InpReleaseChannel`
- `InpBuildProfile`
- `InpStrictReleaseMode`
- `InpHideDebugInRelease`
- `InpMaxDashboardRowsRelease`

## Runtime outputs

- `runtime.product_version`
- `runtime.product_release_channel`
- `runtime.product_build_profile`
- `runtime.product_build_summary`
- `runtime.product_release_gate_summary`

## Rule

The rest of the terminal must not guess release identity. It reads it from the product module.
