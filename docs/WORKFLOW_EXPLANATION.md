

\# SmartCI GitHub Actions Workflow Explanation



\## 1. Introduction



GitHub Actions is used to automate the SmartCI pipeline.



The workflow runs when code is pushed to the main branch, when a pull request is created or updated, or when the workflow is manually triggered.



Workflow file:



`.github/workflows/ci.yml`



\## 2. Workflow Trigger Events



The pipeline supports:



\- Push to main.

\- Pull requests targeting main.

\- Manual execution using workflow\_dispatch.



\## 3. Pipeline Execution Steps



\### Step 1: Checkout Repository



Uses `actions/checkout@v4` to download the repository source code.



Full Git history is fetched to support changed-file detection.



\### Step 2: Set Up Python



Uses `actions/setup-python@v5` to configure Python 3.12.



\### Step 3: Install Dependencies



Installs the Python packages listed in `requirements.txt`.



\### Step 4: Restore SmartCI Cache



Uses `actions/cache@v4` to restore the `.smartci-cache/` directory.



The cache key includes the operating system, Python version, source files, and requirements file.



\### Step 5: Run Smart Build Cache



Runs:



```bash

python -m scripts.cache\_build --output reports/build-cache.json

```



This checks cached build artifacts and rebuilds invalid artifacts.



\### Step 6: Select Related Tests



Runs the dynamic test-selection script using the Git base and head commits.



The script identifies relevant tests based on changed files.



\### Step 7: Run the Full Test Suite



Runs the complete pytest suite as a safety check.



The test output and JUnit report are stored in the reports directory.



\### Step 8: Run ML Failure Prediction



Generates synthetic data, trains the Logistic Regression model, and predicts failure probability.



The prediction is advisory only.



\### Step 9: Summarize Build Logs



Uses the extractive summarizer to process the available build log.



\### Step 10: Upload Reports



Uses `actions/upload-artifact@v4` to upload available reports, including when earlier steps fail.



\## 4. Pipeline Overview



```text

GitHub Push / Pull Request

&#x20;          |

&#x20;          v

&#x20;   Checkout Repository

&#x20;          |

&#x20;          v

&#x20;     Setup Python

&#x20;          |

&#x20;          v

&#x20;  Install Dependencies

&#x20;          |

&#x20;          v

&#x20;   Restore SmartCI Cache

&#x20;          |

&#x20;          v

&#x20;   Smart Build Cache

&#x20;          |

&#x20;          v

&#x20;  Dynamic Test Selection

&#x20;          |

&#x20;          v

&#x20;   Full Pytest Suite

&#x20;          |

&#x20;          v

&#x20;  ML Failure Prediction

&#x20;          |

&#x20;          v

&#x20;  Build Log Summarization

&#x20;          |

&#x20;          v

&#x20;     Upload Reports

```



\## 5. Failure Handling



\- The full test suite is a safety check after test selection.

\- ML prediction runs independently of the test result when dependencies are installed.

\- Report upload is configured to run even if earlier steps fail.

\- Predictions do not automatically block builds.



\## 6. Artifacts and Reports



The workflow can produce:



\- `build-cache.json`

\- `test-selection.json`

\- `junit.xml`

\- `build.log`

\- `log-summary.json`

\- ML prediction and evaluation reports



These reports help inspect pipeline execution.



\## 7. Learning Outcome



This workflow demonstrates:



\- CI automation.

\- GitHub Actions.

\- Dependency installation.

\- Persistent cache restoration.

\- Dynamic test selection.

\- Automated testing.

\- ML-based advisory prediction.

\- Build-log summarization.

\- Artifact upload.



