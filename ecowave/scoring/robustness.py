from __future__ import annotations


def robustness_grade(precrisis_visible: bool, structural_visible: bool) -> str:
    if precrisis_visible and structural_visible:
        return "A"
    if precrisis_visible and not structural_visible:
        return "B"
    if structural_visible and not precrisis_visible:
        return "C"
    return "D"
