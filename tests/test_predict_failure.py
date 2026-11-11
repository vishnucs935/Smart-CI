
import json

import pytest

from ml.predict_failure import FEATURES, generate_dataset, sigmoid


def test_sigmoid_zero():
    assert sigmoid(0) == pytest.approx(0.5)


def test_sigmoid_positive():
    assert sigmoid(2) > 0.5


def test_sigmoid_negative():
    assert sigmoid(-2) < 0.5


def test_feature_list():
    assert "files_changed" in FEATURES
    assert "previous_failure" in FEATURES


def test_generate_dataset_creates_600_records(tmp_path, monkeypatch):
    import ml.predict_failure as prediction

    monkeypatch.setattr(prediction, "DATA_DIR", tmp_path)
    monkeypatch.setattr(prediction, "ROOT", tmp_path)

    generate_dataset()

    records = json.loads(
        (tmp_path / "build_history.json").read_text(encoding="utf-8")
    )

    assert len(records) == 600


def test_dataset_has_required_features(tmp_path, monkeypatch):
    import ml.predict_failure as prediction

    monkeypatch.setattr(prediction, "DATA_DIR", tmp_path)
    monkeypatch.setattr(prediction, "ROOT", tmp_path)

    generate_dataset()

    records = json.loads(
        (tmp_path / "build_history.json").read_text(encoding="utf-8")
    )

    for record in records:
        for feature in FEATURES:
            assert feature in record

        assert record["failure"] in [0, 1]


def test_dataset_generation_is_reproducible(tmp_path, monkeypatch):
    import ml.predict_failure as prediction

    monkeypatch.setattr(prediction, "DATA_DIR", tmp_path)
    monkeypatch.setattr(prediction, "ROOT", tmp_path)

    generate_dataset()

    first = (tmp_path / "build_history.json").read_text(
        encoding="utf-8"
    )

    generate_dataset()

    second = (tmp_path / "build_history.json").read_text(
        encoding="utf-8"
    )

    assert first == second

