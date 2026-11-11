
import pytest

from scripts.summarize_log import (
    redact_secrets,
    extract_failure_facts,
    summarize_log,
    MAX_LOG_SIZE,
)


def test_api_key_is_redacted():
    text = "API_KEY=my_secret_value"

    result = redact_secrets(text)

    assert "my_secret_value" not in result
    assert "[REDACTED]" in result


def test_github_token_is_redacted():
    text = "Token: ghp_abcdefghijklmnopqrstuvwxyz123456"

    result = redact_secrets(text)

    assert "ghp_" not in result
    assert "[REDACTED]" in result


def test_extracts_failure_lines():
    log = """
    Running tests
    test_cart.py FAILED
    AssertionError: Expected 118 but got 100
    2 failed, 10 passed
    """

    facts = extract_failure_facts(log)

    assert len(facts) == 3
    assert any("FAILED" in fact for fact in facts)
    assert any("AssertionError" in fact for fact in facts)


def test_removes_duplicate_failure_lines():
    log = """
    ERROR: Something failed
    ERROR: Something failed
    """

    facts = extract_failure_facts(log)

    assert len(facts) == 1


def test_no_failure_lines():
    log = "Running tests\nAll tests passed\n"

    facts = extract_failure_facts(log)

    assert facts == []


def test_summarize_log_file(tmp_path):
    log_file = tmp_path / "build.log"
    log_file.write_text(
        "test_example FAILED\nAPI_KEY=my_secret_value",
        encoding="utf-8",
    )

    facts = summarize_log(log_file)

    assert any("FAILED" in fact for fact in facts)
    assert all("my_secret_value" not in fact for fact in facts)


def test_missing_log_file():
    with pytest.raises(FileNotFoundError):
        summarize_log("missing-build.log")


def test_log_exceeds_size_limit(tmp_path):
    log_file = tmp_path / "large.log"
    log_file.write_bytes(b"A" * (MAX_LOG_SIZE + 1))

    with pytest.raises(ValueError, match="2 MB"):
        summarize_log(log_file)
