# M0001 Final Node/Random Reports

## Purpose

The compact logRTV node-vs-random report is no longer printed during every
runtime update. It is printed only when the EA finishes (`OnDeinit`).

## Journal output

At the end of the run, exactly two final result prints are produced:

```text
DAL_M0001_FINAL_NODES  *** ... NODES*...
DAL_M0001_FINAL_RANDOM *** ... RANDOM*... *** COMPARE*...
```

The first line is the aggregate for final node/territory events.
The second line is the aggregate for matched random reference windows, plus the
node-vs-random comparison summary.

## Disabled noisy prints

The following are disabled by default:

```text
per-bar DAL M0001 MQL-NATIVE status print
runtime changing compact null report
verbose multi-line distribution report
RTV text file export
empty live stream initialization print
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.55`.
