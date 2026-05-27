# Wave validation rules

A candidate wave requires:

1. at least two independent curves confirming movement;
2. at least one volume-like indicator confirming intensity;
3. robustness against both reference windows;
4. better explanation than plain chronology;
5. the synchronisation/robustness evidence must beat the surrogate null
   (`ecowave/scoring/null_test.py`) — a count that any random segmentation also
   reaches is not validation (see `improvement_roadmap.md` #1).

Grades:

- A: robust
- B: probable
- C: fragile
- D: rejected
