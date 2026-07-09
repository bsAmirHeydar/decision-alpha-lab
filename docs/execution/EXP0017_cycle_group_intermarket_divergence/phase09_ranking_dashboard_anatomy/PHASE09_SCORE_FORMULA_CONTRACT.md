# Phase 09 Score Formula Contract

## Objective

The score is a comparison tool. It is not a trading edge by itself and not execution authority.

## Components

The default quality score is a weighted blend:

```text
quality_score =
  win_rate_score          * weight_win_rate
+ expectancy_score        * weight_average_r
+ normalized_score        * weight_normalized_outcome
+ safety_score            * weight_safety
+ sample_confidence_score * weight_sample_confidence
```

The default weights are:

| Component | Default Weight |
|---|---:|
| Win rate | 0.25 |
| Average R | 0.30 |
| Normalized outcome | 0.15 |
| Safety | 0.20 |
| Sample confidence | 0.10 |

## Component Definitions

### Win-rate score

Directly uses win-rate percent, clamped to 0–100.

### Expectancy score

Maps average R into 0–100:

```text
expectancy_score = clamp(50 + avg_r * 50, 0, 100)
```

### Normalized score

Maps daily-range-normalized outcome into 0–100:

```text
normalized_score = clamp(50 + avg_normalized * 100, 0, 100)
```

### Safety score

Penalizes stop rate and stop streak:

```text
safety_score = clamp(100 - stop_rate_percent - max_stop_streak * 4, 0, 100)
```

### Sample confidence

Measures whether the sample is large enough to take the bucket seriously:

```text
sample_confidence = clamp(sample_count / minimum_sample_for_ranking * 100, 0, 100)
```

## Grades

| Grade | Quality Score |
|---|---:|
| A | >= 80 |
| B | >= 70 |
| C | >= 60 |
| D | >= 50 |
| F | < 50 |

## Shortlist Boundary

A shortlist candidate must pass:

- minimum sample count
- minimum quality score
- minimum win rate
- minimum average R
- maximum stop streak

Shortlist means: review later. It does not mean: execute.
