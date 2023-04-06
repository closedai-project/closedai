import pytest

from closedai import is_transformers_available


def requires_transformers(test_case):
    """
    Decorator marking a test that requires Jinja2.

    These tests are skipped when Jinja2 is not installed.
    """
    if not is_transformers_available():
        return pytest.mark.skip(reason="test requires transformers.")(test_case)
    else:
        return test_case


def test_dummy_pipeline():
    from closedai import DummyPipeline

    pipeline = DummyPipeline()
    assert pipeline.get_completion("Hello") == ", and 1, and 2, and 3, and 4, and 5"

    pipeline = DummyPipeline(duration=3)
    assert pipeline.get_completion("Hello") == ", and 1, and 2, and 3"
