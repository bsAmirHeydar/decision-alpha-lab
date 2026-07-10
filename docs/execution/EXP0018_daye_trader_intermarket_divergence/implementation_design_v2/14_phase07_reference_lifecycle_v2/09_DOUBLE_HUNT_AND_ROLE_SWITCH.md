# Double hunt and role switch

## Double hunt

If both symbols have hunted their own reference side, the divergence basis has ended. The state becomes `RETIRED_DOUBLE_HUNT`.

## Role switch

If the previously protected symbol becomes the one-sided hunter on the same reference, its own reference has necessarily been hunted. The old reference retires as `RETIRED_ROLE_SWITCH`; the role switch is not promoted as a new use of the same retired reference.
