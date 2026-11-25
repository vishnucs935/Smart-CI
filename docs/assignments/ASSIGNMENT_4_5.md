# 4.5 · Build-Failure Prediction

**Objective.** Train and evaluate a model that estimates build-failure risk from information available before a build.

## Procedure

1. Install the project requirements. Run `python -m ml.predict_failure generate` to reproduce 600 synthetic build records using seed 42. Each includes the changed file and line counts, dependency and test changes, previous failure, and a simulated outcome.
2. Run `python -m ml.predict_failure train`. The first 480 examples train a scaler and logistic regression. The final 120 evaluate them. Scaling is fitted only on training records so held-out data cannot influence that step.
3. Read reports/prediction/metrics.json. At a 0.5 threshold the model classified 78 of 120 records correctly (65.0%). Always predicting the most common training label scored 60.8%. Of 47 simulated failures, the model detected 21 and missed 26. Failure recall was 44.7% and F1 was 0.50.
4. Run `python -m ml.predict_failure predict --features ml/example_features.json`. The example received an estimated failure probability of 0.556, just above the threshold. The CI job publishes the metrics and prediction with the other reports.

## Learning

The 65% accuracy hides the missed failures. Comparing recall and a simple baseline gives a clearer picture of the model's usefulness. These results describe simulated data. Evaluating it for this repository would require real earlier builds for training and later builds for evaluation. The score is advisory and the test results decide whether CI passes.
