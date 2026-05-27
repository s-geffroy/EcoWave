from ecowave.config import is_placeholder


def test_placeholder_detection():
    assert is_placeholder("")
    assert is_placeholder("replace_me")
    assert not is_placeholder("abc123")
