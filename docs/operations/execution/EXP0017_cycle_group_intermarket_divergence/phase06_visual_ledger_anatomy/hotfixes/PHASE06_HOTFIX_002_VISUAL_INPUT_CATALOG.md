# Phase 06 Hotfix002 — Visual Input Catalog

## Main switch

```text
InpDrawDivergenceOriginDestinationLine
```

Controls whether the main divergence line is drawn.

## Origin inputs

```text
InpDivergenceOriginSymbolMode
InpDivergenceOriginTimeMode
InpDivergenceOriginPriceMode
```

These inputs define the starting point of the visual divergence leg.

Recommended default:

```text
Symbol: hunter
Time: exact reference extreme
Price: hunter reference price
```

## Destination inputs

```text
InpDivergenceDestinationSymbolMode
InpDivergenceDestinationTimeMode
InpDivergenceDestinationPriceMode
```

These inputs define the ending point of the visual divergence leg.

Recommended default:

```text
Symbol: hunter
Time: exact current-cycle extreme
Price: hunter current-cycle extreme
```

## Marker inputs

```text
InpDrawOriginMarker
InpDrawDestinationMarker
InpOriginMarkerArrowCode
InpDestinationMarkerArrowCode
InpOriginMarkerWidth
InpDestinationMarkerWidth
InpOriginMarkerColor
InpDestinationMarkerColor
```

Markers separate the visual source from the visual destination.

## Vertical inputs

```text
InpDrawOriginVertical
InpDrawDestinationVertical
InpDrawConfirmationMarker
```

These help audit time boundaries.

## Guide inputs

```text
InpDrawHunterReferenceGuide
InpDrawCleanReferenceGuide
InpDrawCleanStopReferenceGuide
InpDrawHunterCurrentExtremeGuide
InpGuideLineStyle
InpGuideLineWidth
InpGuideColor
InpCleanComparisonColor
```

Guides are not trade instructions. They are visual audit helpers.

## Clean comparison inputs

```text
InpDrawCleanComparisonLine
InpDrawCleanComparisonOnlyWhenChartIsCleanSymbol
```

The clean line shows the non-hunted symbol's reference-to-current behavior. It is disabled by default to avoid cross-symbol scale confusion.

## Label inputs

```text
InpDrawTextLabel
InpLabelFontSize
InpLabelOffsetPoints
```

The label is placed near the destination point.
