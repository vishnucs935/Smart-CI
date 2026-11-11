import argparse
import hashlib
import json
import platform
import sys
import py_compile
from pathlib import Path

from scripts.dependencies import (
    build_module_map,
    get_direct_dependencies,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "src"
CACHE_DIR = ROOT / ".smartci-cache"
ARTIFACT_DIR = CACHE_DIR / "artifacts"
RECEIPT_FILE = CACHE_DIR / "receipt.json"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_receipt():
    if not RECEIPT_FILE.exists():
        return {}

    try:
        return json.loads(RECEIPT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def build_cache():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    old_receipt = load_receipt()
    new_receipt = {}

    module_map = build_module_map(ROOT)
    source_files = sorted(SOURCE_DIR.rglob("*.py"))

    requirements = ROOT / "requirements.txt"
    requirements_hash = (
        sha256(requirements.read_bytes()) if requirements.exists() else ""
    )

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "requirements": requirements_hash,
    }

    fingerprints = {}
    visiting = set()
    hits = 0
    misses = 0

    def build_one(source_file):
        nonlocal hits, misses

        module_name = next(
            name for name, path in module_map.items()
            if path == source_file
        )

        if module_name in fingerprints:
            return fingerprints[module_name]

        if module_name in visiting:
            raise ValueError(f"Circular dependency: {module_name}")

        visiting.add(module_name)

        dependencies = get_direct_dependencies(
            source_file, ROOT, module_map
        )

        dependency_hashes = {}

        for dependency in sorted(dependencies):
            dependency_name = next(
                name for name, path in module_map.items()
                if path == dependency
            )
            dependency_hashes[dependency_name] = build_one(dependency)

        data = {
            "source": sha256(source_file.read_bytes()),
            "dependencies": dependency_hashes,
            "environment": environment,
        }

        fingerprint = sha256(
            json.dumps(data, sort_keys=True).encode("utf-8")
        )

        artifact = ARTIFACT_DIR / f"{fingerprint}.pyc"
        previous = old_receipt.get(module_name, {})

        if (
            previous.get("fingerprint") == fingerprint
            and artifact.exists()
            and previous.get("artifact_hash") == sha256(artifact.read_bytes())
        ):
            hits += 1
            status = "HIT"
        else:
            py_compile.compile(
                str(source_file),
                cfile=str(artifact),
                doraise=True,
            )
            misses += 1
            status = "MISS"

        artifact_hash = sha256(artifact.read_bytes())

        new_receipt[module_name] = {
            "fingerprint": fingerprint,
            "artifact": str(artifact.relative_to(ROOT)),
            "artifact_hash": artifact_hash,
        }

        print(f"{status}: {module_name}")

        visiting.remove(module_name)
        fingerprints[module_name] = fingerprint
        return fingerprint

    for source_file in source_files:
        build_one(source_file)

    RECEIPT_FILE.write_text(
        json.dumps(new_receipt, indent=4),
        encoding="utf-8",
    )

    result = {
        "hits": hits,
        "misses": misses,
        "total": hits + misses,
    }

    print("\nCache summary:")
    print(json.dumps(result, indent=4))

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Save cache summary as JSON")
    args = parser.parse_args()

    summary = build_cache()

    if args.output:
        output_path = ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(summary, indent=4),
            encoding="utf-8",
        )
        print(f"Summary saved to {output_path}")
