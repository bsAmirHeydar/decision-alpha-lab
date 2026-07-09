# Post F3 Recognition Families Implemented

The MQL recognition layer must not use one generic `F3H` bucket. It must distinguish:

- `F3H_DIRECT_STRUCTURAL`
- `F3H_DIRECT_GEOMETRIC_80`
- `F3H_DELAYED_STRUCTURAL`
- `F3H_DELAYED_GEOMETRIC_80`

This prevents the chart from showing a plausible but semantically wrong Hook after F3.
