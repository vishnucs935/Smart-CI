

\# Assignment 4.2 – Smart Build-Cache Invalidation



\## 1. Objective



The objective is to avoid rebuilding unchanged Python modules and rebuild modules when their source code or dependencies change.



\## 2. Problem



In a normal build process, unchanged modules may be compiled repeatedly.



This wastes build resources and time.



Smart Build Cache checks whether a previously generated artifact can safely be reused.



\## 3. Implementation



Two Python scripts are used.



\### A. Dependency Graph



File: `scripts/dependencies.py`



Responsibilities:



\- Find Python modules inside the source directory.

\- Read import statements.

\- Build a directed dependency graph.

\- Identify direct and transitive dependencies.



\### B. Build Cache



File: `scripts/cache\_build.py`



Responsibilities:



\- Calculate SHA-256 fingerprints.

\- Include Python runtime and platform information.

\- Include dependency and build-tool fingerprints.

\- Generate checked-hash `.pyc` artifacts.

\- Save SHA-256 receipts.

\- Rebuild missing or corrupted artifacts.



\## 4. How It Works



```text

Python Source Files

&#x20;       |

&#x20;       v

Dependency Graph

&#x20;       |

&#x20;       v

Calculate SHA-256 Keys

&#x20;       |

&#x20;       v

Check Cache Receipt

&#x20;       |

&#x20;       v

Is Artifact Valid?

&#x20;     /     \\

&#x20;   Yes      No

&#x20;    |        |

&#x20;    v        v

&#x20;  Cache    Rebuild

&#x20;   Hit      Artifact

&#x20;     \\       /

&#x20;      v     v

&#x20;     Build Summary

```



\## 5. Commands



Run the build cache:



```powershell

python -m scripts.cache\_build --output reports/build-cache.json

```



Run the same command again to check whether unchanged artifacts are reused.



\## 6. Cache Invalidation



The cache must be invalidated when relevant inputs change.



Examples:



\- Source module changes.

\- A transitive dependency changes.

\- Requirements change.

\- Python runtime or platform changes.

\- A cached artifact is missing or corrupted.



For example, `src/cart.py` imports pricing functions from `src/pricing.py`.



Therefore, a pricing change must invalidate both pricing and cart artifacts.



An unrelated inventory artifact can remain reusable.



\## 7. Verification



The following scenarios should be checked:



1\. First build: cold cache.

2\. Second build: warm cache.

3\. Modify a source module: affected artifacts rebuild.

4\. Modify requirements: artifacts are invalidated.

5\. Corrupt or remove an artifact: artifact is rebuilt.



Record the actual command outputs and results in the evidence folder.



\## 8. Learning Outcome



This assignment demonstrates:



\- Dependency graphs.

\- Content-based hashing.

\- SHA-256 integrity verification.

\- Python bytecode compilation.

\- Cache hits and misses.

\- Safe cache invalidation.



\*\*Note:\*\* Cache reuse counts demonstrate reuse behavior. They do not independently prove a reduction in total CI execution time.



