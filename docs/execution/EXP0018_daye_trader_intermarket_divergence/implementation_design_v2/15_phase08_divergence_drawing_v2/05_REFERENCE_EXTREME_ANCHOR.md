# Reference Extreme Anchor

For a High-side accepted use, point one is the Hunter symbol's actual reference-period High and the source-bar time where that final High occurred. For a Low-side use, point one is the actual Low.

Equal final extremes may occur more than once. The engine stores both first and last occurrence. Default policy is `FIRST_OCCURRENCE`; `LAST_OCCURRENCE` is available as an explicit input. The policy changes only visual placement along an equal-price plateau, never acceptance or lifecycle state.
