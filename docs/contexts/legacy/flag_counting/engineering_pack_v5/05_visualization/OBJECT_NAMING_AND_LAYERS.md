# Object Naming and Layers

## Naming Goals

Chart objects must be deletable, refreshable, and traceable.

Never create anonymous trendlines.

## Prefix

Use one prefix for all Flag Counting objects:

```text
FCN_
```

## Suggested Names

```text
FCN_BODY_LINE1_<f_id>
FCN_BODY_ARC_<f_id>
FCN_LABEL_F_<f_id>
FCN_LABEL_O_<f_id>
FCN_LABEL_NUM_<hook_id>_<n>
FCN_HOOK_ARC_<hook_id>
FCN_PANEL_ROW_<row_id>
```

## Layer Order

Recommended draw order:

1. historical/locked F3 extension background arcs;
2. ND/Hook arcs;
3. flag body lines;
4. origin markers;
5. internal numbers;
6. F labels;
7. panel/status objects.

## Width

Default:

```text
line width = 1
```

Avoid scale-based thickness by default.

## Shades

Use deterministic shade from sequence id:

```text
shade_index = hash(sequence_id) mod N
```

Use shade inside semantic color family.

## Stale Object Cleanup

Renderer receives current render object ids.

On refresh:

1. build set of desired object names;
2. update/create desired objects;
3. delete old FCN_ objects not desired unless locked persistence requires retention;
4. never delete non-FCN objects.

## Locked Persistence

Locked F3 objects should remain if:

```text
InpShowLockedF3 = true
```

Default true.

## Tooltip / Description

Every object should include a description string containing:

```text
chain id
F id or Hook id
level
status
origin/leg1/waist/leg2 node ids
reason emitted
```

This allows chart audit without reading logs every time.
