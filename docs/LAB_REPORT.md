

\# SmartCI Lab Report



\## 1. Introduction



SmartCI is an educational project that demonstrates automation techniques in software development and Continuous Integration.



The project implements four features:



1\. Smart Build-Cache Invalidation.

2\. Dynamic Test-Subset Routing.

3\. Build/Error-Log Summarization.

4\. Build-Failure Prediction.



\## 2. Tools and Technologies



\- Python

\- pytest

\- Git and GitHub

\- GitHub Actions

\- SHA-256

\- Python AST

\- Scikit-learn

\- Logistic Regression

\- JSON



\## 3. Assignment Implementation



\### Assignment 4.2 – Smart Build Cache



Implemented dependency analysis, content-based cache keys, checked-hash bytecode artifacts, and artifact integrity verification.



\### Assignment 4.3 – Dynamic Test Selection



Implemented changed-file analysis and selection of related tests, with documentation-only filtering and safe full-suite fallback.



\### Assignment 4.4 – Log Summarization



Implemented extractive log summarization, sensitive-value redaction, and structured JSON output.



Actual local LLM inference has not yet been verified.



\### Assignment 4.5 – Failure Prediction



Implemented a Logistic Regression model using synthetic build-history data.



The model produces an advisory failure probability.



\## 4. Local Testing Results



The latest previously confirmed complete test run:



\*\*54 tests passed.\*\*



Individual test results previously verified:



| Test module | Passed |

|---|---:|

| `test\_summarize\_log.py` | 8 |

| `test\_predict\_failure.py` | 7 |



Other modules were included in the complete test run.



\## 5. ML Evaluation



| Metric | Result |

|---|---:|

| Accuracy | 0.650 |

| Precision | 0.568 |

| Recall | 0.447 |

| F1 Score | 0.500 |

| ROC-AUC | 0.651 |

| Brier Score | 0.227 |



The evaluation uses synthetic data and should not be interpreted as real-world CI performance.



\## 6. Security and Reliability



\- Sensitive log values are redacted.

\- Cache artifacts are checked before reuse.

\- Unknown test-selection cases use a safe fallback.

\- The complete test suite is retained as a safety check.

\- ML predictions are advisory only.



\## 7. Limitations



\- Build history is synthetic.

\- Local LLM inference is not yet verified.

\- Actual CI execution and uploaded artifacts must be verified on GitHub.

\- Cache reuse does not by itself prove reduced total pipeline time.



\## 8. Conclusion



The SmartCI project demonstrates how build caching, dynamic test selection, log summarization, and ML-based failure prediction can be integrated into a CI workflow.



The project also highlights the importance of testing, artifact integrity, security, and documenting limitations.



