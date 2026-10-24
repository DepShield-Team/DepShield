
import ast
import sys
from pathlib import Path

# Python modules included in the standard library
STDLIB_ALLOWLIST = set(sys.stdlib_module_names)


def extract_python_imports(file_path: str) -> list[dict]:
    """
    Extract external Python imports from a source file.

    Returns:
        A list of dictionaries containing the package name and line number.
    """
    source_path = Path(file_path)
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))

    detected_imports = []
    seen = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]

        elif isinstance(node, ast.ImportFrom):
            # Ignore relative imports and imports without a module name
            if node.level > 0 or not node.module:
                continue
            names = [node.module]

        else:
            continue

        for name in names:
            package = name.split(".")[0]

            if package in STDLIB_ALLOWLIST:
                continue

            if package not in seen:
                seen.add(package)
                detected_imports.append({
                    "package": package,
                    "line": node.lineno
                })

    return detected_imports
