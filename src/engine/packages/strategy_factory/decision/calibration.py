"""Small online-safe probability calibrators."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp


class CalibrationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class IdentityCalibrator:
    def transform(self, probability: float) -> float:
        return min(1.0, max(0.0, float(probability)))


@dataclass(frozen=True, slots=True)
class PlattCalibrator:
    slope: float
    intercept: float

    def transform(self, score: float) -> float:
        z = self.slope * float(score) + self.intercept
        if z >= 0:
            return 1.0 / (1.0 + exp(-z))
        ez = exp(z)
        return ez / (1.0 + ez)


@dataclass(frozen=True, slots=True)
class PiecewiseLinearCalibrator:
    x: tuple[float, ...]
    y: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.x) != len(self.y) or len(self.x) < 2:
            raise CalibrationError("x/y calibration knots require equal length >= 2")
        if any(a >= b for a, b in zip(self.x, self.x[1:])):
            raise CalibrationError("x calibration knots must be strictly increasing")

    def transform(self, value: float) -> float:
        v = float(value)
        if v <= self.x[0]:
            return float(self.y[0])
        if v >= self.x[-1]:
            return float(self.y[-1])
        for i in range(1, len(self.x)):
            if v <= self.x[i]:
                left_x, right_x = self.x[i - 1], self.x[i]
                weight = (v - left_x) / (right_x - left_x)
                result = self.y[i - 1] + weight * (self.y[i] - self.y[i - 1])
                return min(1.0, max(0.0, float(result)))
        return min(1.0, max(0.0, float(self.y[-1])))
