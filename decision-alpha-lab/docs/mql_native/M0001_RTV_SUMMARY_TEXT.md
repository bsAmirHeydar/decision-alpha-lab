# M0001 RTV Summary Comment and Text File

## Chart comment

Every M0001 run now updates the chart comment with the final ready RTV summary:

```text
RTV mean=...
median=...
rtv_ready=...
```

Only events with `rtv_ready=true` are included.

## Text file

The EA writes all final ready RTV rows into a text file:

```text
DAL_M0001_RTV_<symbol>_<timeframe>.txt
```

The writer first attempts the common terminal files area using `FILE_COMMON`, then
falls back to the terminal-local `MQL5/Files` directory.

## Included rows

Each ready RTV event row includes:

```text
id
node_id
type
revisit_id
entry_time
exit_time
event_length
rtv_sample_length
rtv_before_start_index
rtv_inside_end_index
mean_before
mean_inside
rtv
consume_reason
touch_confirmed
hunted
consumed
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.49`.
