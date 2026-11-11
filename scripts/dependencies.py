import ast
from pathlib import Path


def get_module_name(file_path, project_root):
    relative_path = file_path.relative_to(project_root).with_suffix("")
    parts = list(relative_path.parts)

    if parts[-1] == "__init__":
        parts.pop()

    return ".".join(parts)


def build_module_map(project_root):
    module_map = {}

    for file_path in project_root.rglob("*.py"):
        if ".venv" in file_path.parts or ".git" in file_path.parts:
            continue

        module_name = get_module_name(file_path, project_root)
        module_map[module_name] = file_path

    return module_map


def get_direct_dependencies(file_path, project_root, module_map):
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return set()

    dependencies = set()

    for node in ast.walk(tree):
        candidates = []

        if isinstance(node, ast.Import):
            candidates = [alias.name for alias in node.names]

        elif isinstance(node, ast.ImportFrom) and node.module:
            candidates = [node.module]

            for alias in node.names:
                candidates.append(f"{node.module}.{alias.name}")

        for module_name in candidates:
            if module_name in module_map:
                dependency = module_map[module_name]

                if dependency != file_path:
                    dependencies.add(dependency)

    return dependencies


def get_transitive_dependencies(file_path, project_root):
    module_map = build_module_map(project_root)
    visited = set()
    pending = list(
        get_direct_dependencies(file_path, project_root, module_map)
    )

    while pending:
        current_file = pending.pop()

        if current_file in visited:
            continue

        visited.add(current_file)

        new_dependencies = get_direct_dependencies(
            current_file, project_root, module_map
        )

        pending.extend(new_dependencies - visited)

    return visited
