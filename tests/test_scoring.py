from ecowave.scoring.robustness import robustness_grade


def test_robustness_grade():
    assert robustness_grade(True, True) == "A"
    assert robustness_grade(True, False) == "B"
    assert robustness_grade(False, True) == "C"
    assert robustness_grade(False, False) == "D"
