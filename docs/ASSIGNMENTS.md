

\# SmartCI Assignments 4.2–4.5



\## Overview



This project implements four SmartCI features using Python.



The objective is to understand how CI pipelines can improve build reuse, test selection, build-log analysis, and failure prediction.



\## Assignment 4.2 – Smart Build-Cache Invalidation



\*\*Objective:\*\* Avoid rebuilding unchanged Python modules.



Implementation:

\- Build a module dependency graph.

\- Generate checked-hash Python bytecode artifacts.

\- Use SHA-256 hashes to identify changes.

\- Verify cached artifacts before reuse.

\- Rebuild missing or corrupted artifacts.



Main files:

\- `scripts/dependencies.py`

\- `scripts/cache\_build.py`



\## Assignment 4.3 – Dynamic Test-Subset Routing



\*\*Objective:\*\* Select relevant tests based on changed files.



Implementation:

\- Identify changed source files.

\- Find tests that depend on changed modules.

\- Select a changed test file directly.

\- Skip tests for documentation-only changes.

\- Run the full suite when changes are unknown or unsafe.



Main file:

\- `scripts/select\_tests.py`



\## Assignment 4.4 – Build/Error-Log Summarization



\*\*Objective:\*\* Extract useful information from CI build logs.



Implementation:

\- Read build logs.

\- Redact sensitive information.

\- Extract failed tests and error information.

\- Generate a structured JSON summary.

\- Support extractive summarization and an optional local LLM provider.



Main file:

\- `scripts/summarize\_log.py`



Current verified mode: Extractive summarization. Local LLM inference is not yet verified.



\## Assignment 4.5 – Build-Failure Prediction



\*\*Objective:\*\* Estimate the probability of a CI build failure.



Implementation:

\- Generate explicitly synthetic build-history data.

\- Train a Logistic Regression model.

\- Evaluate model performance.

\- Save model parameters as JSON.

\- Predict failure probability from build features.



Main files:

\- `ml/predict\_failure.py`

\- `ml/example\_features.json`



\*\*Important:\*\* The prediction is advisory only. Synthetic-data results do not establish real-world CI reliability.



\## Testing



Run the complete test suite:



```powershell

python -m pytest -v

```



Latest local verification: 54 tests passed.



