# English Transcription of the Original RTHP Domain Context

Status: non-canonical source evidence. The source was originally written in Persian. This file is an exact English semantic transcription for repository use. Canonical authority belongs to the accepted RTHP Context contracts.

## Core idea

RTHP is based on divergence between two symbols. A divergence exists when a corresponding cycle High is hunted or touched by one symbol and not by the other. The analogous Low-side relationship is defined in the same way. A Hunt requires only a touch; a close beyond the level is not required. All stated times are New York times.

## Strategy cycles

- L: 07:00:00-09:29:59
- N: 09:30:00-15:59:59
- A: 16:00:00-20:00:00
- L + N + A: the strategy's daytime composite range
- Daily: 20:00:00-19:59:59
- Weekly: Sunday + Monday + Tuesday + Wednesday + Thursday + Friday

At the beginning of the weekly candle, Sunday covers 18:00:00-19:59:59. Monday then runs from 20:00:00 to 19:59:59 for a full 24-hour trading day. Tuesday through Thursday follow the same structure. Friday begins at 20:00:00 on Thursday and continues until 16:59:59 on Friday. The Friday A session is incomplete, just as Sunday contains only a short two-hour segment.

## Named relationship families in the source

- WW: divergence between the current week and the prior week.
- DD: divergence between the current Daily cycle and prior Daily cycles.
- NN: divergence between today's N cycle and prior N cycles.
- LN: divergence between today's N cycle and today's or prior L cycles.
- AN: divergence between today's N cycle and prior A cycles.
- NL: divergence between today's L cycle and prior N cycles.
- NA: divergence between today's A cycle and prior N cycles.
- FCR: divergence between 09:30:00-09:59:59 and 10:00:00-15:59:59.
- PMI: divergence between 07:00:00-09:29:59 and 09:30:00-15:59:59.
- PP: divergence between 09:00:00-09:29:59 and 09:30:00-15:59:59.
- M15 Cycle Group: divergence among 15-minute cycles inside 09:30:00-16:00:00, including sequential and non-sequential pairs. Sequential means two adjacent 15-minute cycles.

Multiple Bullish and Bearish divergence families may be present at the same M15 evaluation cut, and each is counted. The default evaluation timeframe in the source is M15.

## Lookback and incomplete history

For DD, NN, LN, AN, NL, and NA, the source proposes a default lookback of 12 prior days or cycles. If an expiry-based chart or newly listed contract contains fewer than 12 prior observations, the evaluator must process only the available observations and must not fail. Missing Saturdays must not create errors or artificial cycles.

## First touch, persistence, and reference consumption

If the same prior High is swept multiple times, only the first sweep is primary. A line created for the first confirmed divergence should remain visible even after the divergence relationship later resolves.

After the symbol that was initially protected later touches its own corresponding High or Low, that scoped reference can no longer create a new divergence for the same applicable relationship scope. While the protected side remains untouched, later active cycles may still form new divergence occurrences against that reference, subject to independent occurrence identity.

The source mentions earlier code as possible evidence for this lifecycle rule, but no repository path, commit, or file digest was supplied. Therefore the previous code has no canonical authority.
