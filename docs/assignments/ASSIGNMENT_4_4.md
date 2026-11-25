# 4.4 · LLM-Based Build/Error-Log Summarization

**Objective.** Turn a failed CI log into a short diagnostic and retain the evidence needed to verify the model's answer.

## Procedure

1. Open docs/evidence/pytest-failure.txt. This is the failed pytest step from Part 4.1, run 45601805118. At line 11 of test_pricing.py, the expected value was deliberately changed to 101.0. The function returned 100.0.
2. On Python 3.12, install a CPU model runtime with `python -m pip install torch --index-url https://download.pytorch.org/whl/cpu`, then `python -m pip install -r requirements-llm.txt`. Run the command below from the repository root. The first run downloads the pinned FLAN-T5-small model.
3. Read the JSON output. The program redacts common credential patterns and extracts the failed test, file location, assertion and test counts. It prompts the local model for a short diagnosis and records the model revision and prompt hash. No hosted inference account is required.
4. Compare the output with the failed step. The recorded inference returned “100.0 == 101.0”. The summary paired it with the verified outcome of one failed and nine passed. The source identifies the fix: restore the expected zero-discount result to 100.0. The model itself supplied no explanation of the pricing rule.

```bash
python -m scripts.summarize_log docs/evidence/pytest-failure.txt --provider local-llm --output reports/llm-summary.json
```

## Learning

The model highlighted the mismatch, but the original assertion explained which value was expected. Keeping evidence and generated text in separate fields makes that distinction visible. Ordinary CI runs use inexpensive extraction. A manually dispatched CI run also invokes the model on the recorded failure. The verified model output is included at docs/evidence/llm-summary.json.
