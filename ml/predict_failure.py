
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "ml"
REPORT_DIR = ROOT / "reports" / "prediction"

FEATURES = [
    "files_changed",
    "lines_changed",
    "dependency_changed",
    "tests_changed",
    "previous_failure",
]


def generate_dataset():
    """Generate 600 reproducible synthetic build records."""

    random.seed(42)
    records = []

    for _ in range(600):
        files = random.randint(1, 30)
        lines = random.randint(10, 1500)
        dependency = random.randint(0, 1)
        tests = random.randint(0, 1)
        previous = random.randint(0, 1)

        risk = (
            -2.5
            + files * 0.035
            + lines * 0.001
            + dependency * 0.8
            - tests * 0.3
            + previous * 0.9
        )

        probability = 1 / (1 + pow(2.71828, -risk))
        failure = 1 if random.random() < probability else 0

        records.append({
            "files_changed": files,
            "lines_changed": lines,
            "dependency_changed": dependency,
            "tests_changed": tests,
            "previous_failure": previous,
            "failure": failure,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output = DATA_DIR / "build_history.json"
    output.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )

    print(f"Generated {len(records)} records.")
    print(f"Saved: {output.relative_to(ROOT)}")


def sigmoid(value):
    return 1 / (1 + pow(2.71828, -value))


def train_model():
    """Train logistic regression using chronological data."""

    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
            brier_score_loss,
            confusion_matrix,
        )
    except ImportError:
        raise SystemExit(
            "Install scikit-learn first: "
            "python -m pip install scikit-learn"
        )

    data_file = DATA_DIR / "build_history.json"

    if not data_file.exists():
        raise FileNotFoundError(
            "Dataset missing. Run generate first."
        )

    records = json.loads(data_file.read_text(encoding="utf-8"))

    X = [[record[name] for name in FEATURES] for record in records]
    y = [record["failure"] for record in records]

    split = int(len(records) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)

    probabilities = model.predict_proba(X_test_scaled)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    metrics = {
        "data_provenance": ["synthetic_seed_42"],
        "warning": (
            "Educational evaluation; synthetic-data metrics "
            "do not establish real CI reliability."
        ),
        "split": "First 80% train, final 20% test; chronological",
        "train_count": len(X_train),
        "test_count": len(X_test),
        "threshold": 0.5,
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "f1": float(
            f1_score(y_test, predictions, zero_division=0)
        ),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "brier_score": float(
            brier_score_loss(y_test, probabilities)
        ),
        "baseline_accuracy": float(
            max(y_test.count(0), y_test.count(1)) / len(y_test)
        ),
        "confusion_matrix_labels": [0, 1],
        "confusion_matrix": confusion_matrix(
            y_test, predictions, labels=[0, 1]
        ).tolist(),
    }

    model_data = {
        "schema": 1,
        "features": FEATURES,
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "coefficients": model.coef_[0].tolist(),
        "intercept": float(model.intercept_[0]),
        "threshold": 0.5,
        "training_provenance": ["synthetic_seed_42"],
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    (REPORT_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    (REPORT_DIR / "model.json").write_text(
        json.dumps(model_data, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(metrics, indent=2))
    print("Model and metrics saved.")


def predict(features_file):
    """Predict failure probability from a feature JSON file."""

    model_file = REPORT_DIR / "model.json"

    if not model_file.exists():
        raise FileNotFoundError(
            "Model missing. Run train first."
        )

    model = json.loads(model_file.read_text(encoding="utf-8"))
    features = json.loads(
        Path(features_file).read_text(encoding="utf-8")
    )

    values = []

    for name in FEATURES:
        if name not in features:
            raise ValueError(f"Missing feature: {name}")

        values.append(float(features[name]))

    scaled = [
        (value - mean) / scale
        for value, mean, scale in zip(
            values,
            model["mean"],
            model["scale"],
        )
    ]

    score = model["intercept"] + sum(
        weight * value
        for weight, value in zip(
            model["coefficients"],
            scaled,
        )
    )

    probability = sigmoid(score)

    result = {
        "failure_probability": probability,
        "prediction": (
            "failure"
            if probability >= model["threshold"]
            else "success"
        ),
        "advisory_only": True,
        "warning": (
            "This educational prediction uses synthetic data. "
            "Never block or skip a build based on this result."
        ),
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output = REPORT_DIR / "prediction.json"
    output.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))
    print(f"Saved: {output.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(
        description="Educational build-failure prediction."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("generate")
    subparsers.add_parser("train")

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument(
        "--features",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "generate":
        generate_dataset()

    elif args.command == "train":
        train_model()

    elif args.command == "predict":
        predict(args.features)


if __name__ == "__main__":
    main()
