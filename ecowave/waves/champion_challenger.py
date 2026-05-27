from __future__ import annotations


def champion_challenger_rule(scores: dict[str, float]) -> str:
    """Return winning model code if scores are available."""
    if not scores:
        return "blocked"
    return max(scores.items(), key=lambda item: item[1])[0]
