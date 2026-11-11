

\# Assignment 4.4 – Build/Error-Log Summarization



\## 1. Objective



The objective is to extract useful information from software build and test logs.



The summary helps developers identify build failures and understand test errors.



\## 2. Problem



Build logs can contain many lines of output.



Finding the important error information manually can take time.



A log summarizer extracts important facts and produces a structured report.



\## 3. Implementation



Main file: `scripts/summarize\_log.py`



Responsibilities:



\- Read build log files.

\- Limit the maximum input size.

\- Redact sensitive information.

\- Identify build status.

\- Extract failed test information.

\- Extract assertion messages and test summaries.

\- Generate a JSON report.



\## 4. Summarization Modes



\### Extractive mode



Extracts facts directly from the supplied log.



It does not call an AI model.



Command:



```powershell

python -m scripts.summarize\_log reports/sample-build.log --provider extractive

```



\### Local LLM mode



An optional local language model can generate an additional explanation.



The model must be installed and actual inference must be executed before claiming this feature is verified.



\## 5. Example Verification



The sample log was processed using extractive mode.



Observed information:



\- Build status: failure.

\- Test summary: 2 failed, 10 passed.

\- API key: redacted.

\- Provider: extractive.

\- LLM used: false.



The output was saved to:



`reports/log-summary.json`



\## 6. Security Considerations



\- Sensitive values must be redacted.

\- Log content must be treated as untrusted data.

\- Model-generated explanations are advisory.

\- Model output must be checked against extracted facts.

\- Log instructions must never be executed.

\- Large log files must be bounded.



\## 7. Testing



Run:



```powershell

python -m pytest tests/test\_summarize\_log.py -v

```



Actual local result: 8 tests passed.



\## 8. Learning Outcome



This assignment demonstrates:



\- Log parsing.

\- Structured error extraction.

\- Secret redaction.

\- JSON report generation.

\- Deterministic summarization.

\- Safe use of optional local language models.



\*\*Verification status:\*\* Extractive summarization and its unit tests are verified. Actual local LLM inference is not yet verified.



