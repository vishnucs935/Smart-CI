

\# Assignment 4.5 – Build-Failure Prediction



\## 1. Objective



The objective is to estimate the probability that a future CI build may fail using historical build information.



\## 2. Problem



CI pipelines execute builds and tests repeatedly.



Predicting possible failures can help developers identify risky builds and investigate them earlier.



\## 3. Implementation



Main file: `ml/predict\_failure.py`



The implementation uses:



\- Synthetic build-history data.

\- Five build-related input features.

\- StandardScaler for feature scaling.

\- Logistic Regression for classification.

\- A chronological training and testing split.

\- JSON files to save model information and predictions.



\## 4. Model Workflow



```text

Synthetic Build History

&#x20;         |

&#x20;         v

&#x20;  Prepare Features

&#x20;         |

&#x20;         v

&#x20;   Scale Features

&#x20;         |

&#x20;         v

&#x20; Train Logistic Regression

&#x20;         |

&#x20;         v

&#x20;   Evaluate Model

&#x20;         |

&#x20;         v

&#x20; Save Model Parameters

&#x20;         |

&#x20;         v

&#x20;Predict Failure Probability

```



\## 5. Commands



\### Generate synthetic data



```powershell

python -m ml.predict\_failure generate

```



\### Train the model



```powershell

python -m ml.predict\_failure train

```



\### Predict build failure



```powershell

python -m ml.predict\_failure predict --features ml/example\_features.json

```



\## 6. Actual Model Evaluation



The local synthetic-data experiment produced:



| Metric | Result |

|---|---:|

| Accuracy | 0.65 |

| Precision | 0.568 |

| Recall | 0.447 |

| F1 Score | 0.500 |

| ROC-AUC | 0.651 |

| Brier Score | 0.227 |

| Baseline Accuracy | 0.608 |



These metrics describe the experiment using synthetic data only.



\## 7. Example Prediction



The example prediction produced:



\- Failure probability: approximately 0.556.

\- Prediction: failure.

\- Advisory only: true.



The result was saved to:



`reports/prediction/prediction.json`



\## 8. Important Limitation



The training data is synthetic.



Therefore:



\- The model is educational.

\- Results do not prove real-world CI prediction accuracy.

\- Predictions must not automatically block or skip builds.

\- Developers must investigate actual build results.



\## 9. Testing



Run:



```powershell

python -m pytest tests/test\_predict\_failure.py -v

```



Actual local result: 7 tests passed.



\## 10. Learning Outcome



This assignment demonstrates:



\- Synthetic dataset generation.

\- Feature scaling.

\- Logistic Regression.

\- Model evaluation.

\- JSON model serialization.

\- Failure probability prediction.

\- Responsible use of ML predictions.



