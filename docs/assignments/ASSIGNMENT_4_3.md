

\# Assignment 4.3 – Dynamic Test-Subset Routing



\## 1. Objective



The objective is to select and run relevant tests based on the files changed in a project.



This helps avoid running unnecessary tests for every small code change.



\## 2. Problem



In a large software project, running the complete test suite after every change can consume unnecessary resources.



Dynamic Test Selection identifies which tests are related to the changed files.



\## 3. Implementation



Main file: `scripts/select\_tests.py`



Responsibilities:



\- Identify changed files.

\- Analyze Python module dependencies.

\- Find tests related to changed source files.

\- Select a changed test file directly.

\- Skip tests for documentation-only changes.

\- Use a full-suite fallback for unknown or unsafe changes.



\## 4. How It Works



```text

Changed Files

&#x20;     |

&#x20;     v

Identify File Type

&#x20;     |

&#x20;     v

Analyze Dependencies

&#x20;     |

&#x20;     v

Select Related Tests

&#x20;     |

&#x20;     v

Choose Execution Mode

&#x20;  /       |        \\

&#x20;Tests   No Tests   Full Suite

```



\## 5. Commands and Verification



\### Case 1: Source file changed



```powershell

python -m scripts.select\_tests --changed src/pricing.py --report reports/test-selection.json

```



Observed result:



\- `tests/test\_pricing.py`

\- `tests/test\_cart.py`



\### Case 2: Documentation changed



```powershell

python -m scripts.select\_tests --changed README.md --report reports/test-selection.json

```



Observed result:



\- Documentation-only change.

\- No tests selected.



\### Case 3: Test file changed



```powershell

python -m scripts.select\_tests --changed tests/test\_pricing.py --report reports/test-selection.json

```



Observed result:



\- Only `tests/test\_pricing.py` selected.



\### Case 4: Unknown file changed



```powershell

python -m scripts.select\_tests --changed random\_file.xyz --report reports/test-selection.json

```



Observed result:



\- Configuration or unknown file changed.

\- Full test suite selected.



\## 6. Safety



The full test suite must still run as a safety check in the CI workflow.



Unknown files and unsafe dependency analysis must not silently skip tests.



\## 7. Learning Outcome



This assignment demonstrates:



\- Static dependency analysis.

\- Changed-file detection.

\- Test selection.

\- Documentation-only filtering.

\- Safe full-suite fallback.



\*\*Note:\*\* Test selection is demonstrated locally. End-to-end CI speed improvements have not been established.



