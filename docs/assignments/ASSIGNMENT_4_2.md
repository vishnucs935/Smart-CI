# 4.2 · Smart Build-Cache Invalidation

**Objective.** Reuse compiled Python modules across CI runs and rebuild a module when a change affects its output.

## Procedure

1. From the repository root, install the dependencies with `python -m pip install -r requirements.txt`. Start in a fresh checkout and run `python -m scripts.cache_build`. The script reads the four Python files in src and compiles each to bytecode. The first run reported four misses.
2. Run the same command again. Each receipt records the source and dependency fingerprint, interpreter, platform, requirements digest and compiled artifact checksum. All four artifacts were reused on the second run.
3. Run `python -m pytest -s tests/test_cache_build.py`. This experiment uses an isolated copy of a four-module example. It edits pricing while keeping cart's import of pricing. The observed result was two misses and two hits. Pricing and cart rebuilt, while inventory and the package initializer remained reusable.
4. Inspect the **Compile changed modules** step in GitHub Actions. The workflow restores a previous cache when available, then verifies each module individually before reuse. The downloadable CI artifact includes the totals in build-cache.json.

## Learning

A hash of cart.py alone misses a change to pricing.py. Including the dependency fingerprint propagates the change to cart. Checking the compiled file separately also catches a missing or damaged artifact. This example follows static imports and assumes an acyclic build graph.
