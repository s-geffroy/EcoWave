"""Shared dataclasses for the forecasting module.

The contract for every forecaster:

- Input: a 1-D numpy array of historical observations sampled at a
  regular cadence (monthly, quarterly, or annual — the cadence is
  implicit in the data, not in the API).
- Output: a :class:`ProbabilisticForecast` carrying the requested
  horizons, the point forecast (sample-mean) for each horizon, and
  the full Monte Carlo sample matrix (n_samples, n_horizons) drawn
  from the model's predictive distribution.

The sample-based representation is the lingua franca. Empirical CRPS,
forecast-interval coverage, and tail coverage all consume the sample
matrix and are therefore distribution-free. Models that have a
closed-form Gaussian predictive density (e.g. AR(1), HAR with Gaussian
residuals) simply draw exact samples from that density; models with
intrinsically simulation-only predictives (MSM, agent-based) draw paths.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ProbabilisticForecast:
    """A probabilistic forecast at one or more horizons.

    Attributes
    ----------
    horizons:
        Horizons (in cadence steps) at which forecasts are produced.
        Length ``H``.
    samples:
        Monte Carlo paths from the predictive distribution. Shape
        ``(n_samples, H)``. ``samples[i, h]`` is the *level* (not the
        increment) forecast at horizon ``horizons[h]`` for path ``i``.
    model_name:
        Short identifier for diagnostics, e.g. ``"rw"``, ``"ar1"``,
        ``"har"``.
    """

    horizons: tuple[int, ...]
    samples: np.ndarray
    model_name: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.samples.ndim != 2:
            raise ValueError(
                f"samples must be 2-D (n_samples, H); got shape {self.samples.shape}"
            )
        if self.samples.shape[1] != len(self.horizons):
            raise ValueError(
                f"samples width {self.samples.shape[1]} != len(horizons) {len(self.horizons)}"
            )
        if any(h <= 0 for h in self.horizons):
            raise ValueError(f"horizons must be positive; got {self.horizons}")

    @property
    def n_samples(self) -> int:
        return int(self.samples.shape[0])

    @property
    def mean(self) -> np.ndarray:
        """Point forecast for each horizon — sample mean."""
        return self.samples.mean(axis=0)

    def quantile(self, q: float | Sequence[float]) -> np.ndarray:
        """Forecast quantile(s) per horizon.

        Returns shape ``(H,)`` for a scalar ``q``, otherwise
        ``(len(q), H)``.
        """
        return np.quantile(self.samples, q, axis=0)

    def at(self, horizon: int) -> np.ndarray:
        """Return the 1-D sample vector for a specific horizon."""
        try:
            index = self.horizons.index(horizon)
        except ValueError as exc:
            raise KeyError(f"horizon {horizon} not in forecast") from exc
        return self.samples[:, index]
