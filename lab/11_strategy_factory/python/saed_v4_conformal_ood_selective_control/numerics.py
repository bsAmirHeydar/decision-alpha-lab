from __future__ import annotations
import math
import random
import statistics

def clamp(value, lower=0.0, upper=1.0):
    return min(float(upper), max(float(lower), float(value)))

def mean(values):
    values = list(map(float, values))
    return sum(values) / len(values) if values else 0.0

def quantile(values, q):
    ordered = sorted(map(float, values))
    if not ordered:
        return 0.0
    position = clamp(q) * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight

def conformal_quantile(scores, alpha):
    ordered = sorted(map(float, scores))
    if not ordered:
        raise ValueError('empty conformal calibration scores')
    rank = int(math.ceil((len(ordered) + 1) * (1.0 - float(alpha))))
    rank = min(len(ordered), max(1, rank))
    return ordered[rank - 1]

def median(values):
    values = list(map(float, values))
    return statistics.median(values) if values else 0.0

def mad(values, center=None):
    values = list(map(float, values))
    if not values:
        return 0.0
    center = median(values) if center is None else float(center)
    return median(abs(value - center) for value in values)

def robust_z(value, center, scale, floor=1e-9):
    denominator = max(float(scale) * 1.4826, float(floor))
    return abs(float(value) - float(center)) / denominator

def empirical_upper_pvalue(calibration_scores, score):
    calibration_scores = list(map(float, calibration_scores))
    if not calibration_scores:
        return 0.0
    return (1.0 + sum(item >= float(score) for item in calibration_scores)) / (len(calibration_scores) + 1.0)

def trapz(points):
    ordered = sorted((float(x), float(y)) for x, y in points)
    return sum((ordered[index][0] - ordered[index - 1][0]) * (ordered[index][1] + ordered[index - 1][1]) / 2.0 for index in range(1, len(ordered)))

def psi(reference, current, bins=10, epsilon=1e-8):
    reference = list(map(float, reference))
    current = list(map(float, current))
    if not reference or not current:
        return 0.0
    edges = [quantile(reference, index / bins) for index in range(1, bins)]
    def proportions(values):
        counts = [0] * bins
        for value in values:
            index = 0
            while index < len(edges) and value > edges[index]:
                index += 1
            counts[index] += 1
        return [max(epsilon, count / len(values)) for count in counts]
    base = proportions(reference)
    observed = proportions(current)
    return sum((q - p) * math.log(q / p) for p, q in zip(base, observed))

def cluster_bootstrap_binary(records, accepted_ids, seed=424, draws=300, alpha=0.10):
    clusters = {}
    accepted_ids = set(accepted_ids)
    for record in records:
        clusters.setdefault(record['cluster_id'], []).append(record)
    names = sorted(clusters)
    if not names:
        return {'draws': 0, 'lower': 0.0, 'upper': 0.0, 'mean': 0.0}
    rng = random.Random(int(seed))
    estimates = []
    for _ in range(int(draws)):
        sampled = [clusters[names[rng.randrange(len(names))]] for _ in names]
        selected = [record for group in sampled for record in group if record['record_id'] in accepted_ids]
        estimates.append(mean(1.0 if record['realized_value'] < 0 else 0.0 for record in selected) if selected else 0.0)
    return {'draws': int(draws), 'lower': quantile(estimates, alpha / 2.0), 'upper': quantile(estimates, 1.0 - alpha / 2.0), 'mean': mean(estimates)}
