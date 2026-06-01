"""Forecasting benchmark module — Roadmap #20.

The CPV verdict (PRs #23-#29) is that the empirical cluster of structural
signatures is C (long memory) + B (multifractality) + D (non-linearity)
+ I (information structure) + S (reflexive regime drift). This module is
the constructive counterpart to that destructive verdict: a benchmark of
candidate models that reproduce parts of the cluster, evaluated against
random-walk and AR baselines on the same panels CPV was estimated on.

Models implemented (incremental delivery):

- ``baselines`` — random walk, AR(1), ARMA(1,1).
- ``har`` — Heterogeneous Autoregressive (Corsi 2009 *J. Financial
  Econometrics*), the workhorse baseline for long-memory-by-aggregation.
- ``arfima_rs`` — ARFIMA (Granger-Joyeux 1980; Hosking 1981) plus
  Markov regime-switching (Bhardwaj-Swanson 2006). [PR B — pending]
- ``msm`` — Markov-Switching Multifractal (Calvet-Fisher 2002, 2004,
  2008). [PR C — pending]

All forecasters share a single probabilistic interface
(``ProbabilisticForecast``) — every model returns a Monte Carlo sample
matrix indexed by (sample, horizon). This sample-based representation is
what allows :mod:`.proper_scoring` to evaluate empirical CRPS (Gneiting-
Raftery 2007), forecast-interval coverage, and tail coverage in a
distribution-free way — important under the heavy tails the CPV cluster
documents.

Cf. ``methodology/feuille_de_route.md`` item #20 for the acceptance
criterion (at least one model from the cluster must beat random walk on
out-of-sample CRPS at 12-month horizon, on ≥ 50 % of variables).
"""
from __future__ import annotations

from ecowave.forecasting.types import ProbabilisticForecast


__all__ = ["ProbabilisticForecast"]
