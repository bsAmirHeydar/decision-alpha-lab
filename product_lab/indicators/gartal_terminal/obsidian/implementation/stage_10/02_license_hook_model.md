# License Hook Model

Stage 10 adds only a license gate location. It is not final anti-piracy.

## Modes

```text
OFF       development/internal
OPTIONAL  beta/demo/audit
REQUIRED  customer/stable
```

## Why a hook now

Licensing must be integrated early because it affects initialization, customer messaging, release packaging, and support. It must not be bolted onto the parser or dashboard later.

## Future upgrade

Replace the placeholder validator with a signed license file or server-issued key that binds product, version, user, expiry, and machine profile.
