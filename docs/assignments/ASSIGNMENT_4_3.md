# 4.3 · Dynamic Test-Subset Routing

**Objective.** Select the tests affected by a change and use the full suite when the impact is uncertain.

## Procedure

1. Install the project requirements. Run `python -m scripts.select_tests --changed src/pricing.py --run`. The router follows imports from each test through the application. It selected test_pricing.py and test_cart.py. All seven selected cases passed.
2. Run `python -m scripts.select_tests --changed src/inventory.py --run`. Inventory has no dependency on pricing. The router selected the three inventory tests.
3. Compare `python -m scripts.select_tests --changed README.md` with `python -m scripts.select_tests --changed requirements.txt`. The README edit selected no tests. The environment change selected the full suite. Shared fixtures, deleted source files and an unavailable Git base also trigger the full suite.
4. On a push or pull request, inspect **Run affected tests**. The workflow passes the base and head revisions to the router. Read reports/test-selection.json in the CI artifact to see the changed paths, reason, mode and selected tests.

## Learning

Matching filenames would miss the cart tests when pricing changes. Transitive imports explain why those tests belong in the selection. Static analysis has limits around dynamic imports and plugins. Changes to shared configuration therefore use the full suite in this exercise.
