
import argparse
import json
import subprocess
import sys
from pathlib import Path

from scripts.dependencies import get_transitive_dependencies


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests"


def get_changed_files(args):
    if args.changed:
        return args.changed

    if not args.base:
        raise ValueError("Missing Git base commit")

    base = args.base

    if args.merge_base:
        result = subprocess.run(
            ["git", "merge-base", args.base, args.head],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        base = result.stdout.strip()

    result = subprocess.run(
        [
            "git", "diff",
            "--name-status",
            "-z",
            base,
            args.head,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    entries = result.stdout.split("\0")
    changed_files = []
    index = 0

    while index < len(entries):
        status = entries[index]
        index += 1

        if not status:
            continue

        if status.startswith(("R", "C")):
            if index + 1 >= len(entries):
                raise ValueError("Incomplete rename information")

            changed_files.append(entries[index])
            changed_files.append(entries[index + 1])
            index += 2
        else:
            if index >= len(entries):
                raise ValueError("Missing changed file path")

            changed_files.append(entries[index])
            index += 1

    return changed_files


def select_tests(changed_files):
    selected = set()
    changed_sources = set()

    if not changed_files:
        return "full", selected, "Missing change history"

    for name in changed_files:
        normalized = name.replace("\\", "/")
        path = Path(normalized)

        if path.is_absolute() or ".." in path.parts:
            return "full", set(), "Unsafe changed path"

        full_path = ROOT / path

        if normalized.startswith("docs/") or normalized in {
            "README.md",
            "LICENSE",
            "CHANGELOG.md"
        }:
            continue

        if normalized.startswith("tests/"):
            if not normalized.endswith(".py"):
                return "full", set(), "Unknown test-related file"

            if not full_path.is_file():
                return "full", set(), "Deleted test file"

            selected.add(full_path)
            continue

        if normalized.startswith("src/"):
            if not normalized.endswith(".py"):
                return "full", set(), "Unknown source-related file"

            if not full_path.is_file():
                return "full", set(), "Deleted source file"

            if path.name == "__init__.py":
                return "full", set(), "Package initialization changed"

            changed_sources.add(full_path)
            continue

        return "full", set(), "Configuration or unknown file changed"

    if changed_sources:
        for test_file in TEST_DIR.glob("test_*.py"):
            try:
                dependencies = get_transitive_dependencies(
                    test_file, ROOT
                )
            except (OSError, ValueError):
                return "full", set(), "Could not analyze test dependencies"

            if any(source in dependencies for source in changed_sources):
                selected.add(test_file)

        if not selected:
            return "full", set(), "No related tests found"

        return "selected", selected, "Related tests found"

    if selected:
        return "selected", selected, "Test files changed"

    return "none", set(), "Documentation-only change"


def write_report(mode, selected, reason, changed_files, report_path):
    report = {
        "mode": mode,
        "reason": reason,
        "changed_files": changed_files,
        "selected_tests": sorted(
            str(path.relative_to(ROOT)) for path in selected
        ),
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--changed", nargs="*", default=[])
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--merge-base", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument(
        "--report",
        default="reports/test-selection.json",
    )

    args = parser.parse_args()

    try:
        changed_files = get_changed_files(args)
        mode, selected, reason = select_tests(changed_files)

    except (ValueError, subprocess.SubprocessError, OSError):
        changed_files = []
        mode, selected, reason = (
            "full",
            set(),
            "Could not identify changed files",
        )

    print(f"Selection reason: {reason}")

    test_paths = sorted(
        str(path.relative_to(ROOT)) for path in selected
    )

    if mode == "none":
        print("No tests selected.")

    elif mode == "full":
        print("Running the full test suite.")

    else:
        print("Selected tests:")
        for path in test_paths:
            print(f"  {path}")

    write_report(
        mode,
        selected,
        reason,
        changed_files,
        ROOT / args.report,
    )

    print(f"Selection report saved: {args.report}")

    if args.run:
        if mode == "none":
            print("Subset test execution skipped.")
        else:
            command = [sys.executable, "-m", "pytest", "-v"]

            if mode == "selected":
                command.extend(test_paths)

            sys.exit(subprocess.call(command, cwd=ROOT))


if __name__ == "__main__":
    main()

