
from pathlib import Path

import tree_sitter_javascript
import tree_sitter_typescript
from tree_sitter import Language, Parser


JS_LANGUAGE = Language(tree_sitter_javascript.language())
TS_LANGUAGE = Language(tree_sitter_typescript.language_typescript())
TSX_LANGUAGE = Language(tree_sitter_typescript.language_tsx())

NODE_BUILTINS = {
    "assert", "buffer", "child_process", "crypto", "events",
    "fs", "http", "https", "module", "os", "path", "process",
    "querystring", "stream", "timers", "tls", "url", "util",
    "zlib", "worker_threads", "readline", "net", "dns",
    "cluster", "vm", "tty", "string_decoder", "perf_hooks",
}


def _get_language(file_path: Path):
    suffix = file_path.suffix.lower()

    if suffix in {".ts"}:
        return TS_LANGUAGE
    if suffix in {".tsx"}:
        return TSX_LANGUAGE
    return JS_LANGUAGE


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def extract_javascript_imports(file_path: str) -> list[dict]:
    """
    Extract external package imports from JavaScript/TypeScript files.

    Returns dictionaries with package names and source line numbers.
    """
    source_path = Path(file_path)
    source = source_path.read_bytes()

    parser = Parser(_get_language(source_path))
    tree = parser.parse(source)

    detected_imports = []
    seen = set()

    for node in _walk(tree.root_node):
        package_name = None

        # import x from "package"; or import "package";
        if node.type == "import_statement":
            for child in node.children:
                if child.type == "string":
                    package_name = child.text.decode("utf-8")[1:-1]
                    break

        # export { x } from "package";
        elif node.type == "export_statement":
            for child in node.children:
                if child.type == "string":
                    package_name = child.text.decode("utf-8")[1:-1]
                    break

        # require("package")
        elif node.type == "call_expression":
            function_node = node.child_by_field_name("function")
            arguments_node = node.child_by_field_name("arguments")

            if (
                function_node
                and function_node.type == "identifier"
                and function_node.text == b"require"
                and arguments_node
                and arguments_node.named_children
            ):
                first_arg = arguments_node.named_children[0]
                if first_arg.type == "string":
                    package_name = first_arg.text.decode("utf-8")[1:-1]

        # import("package")
        elif node.type == "import":
            parent = node.parent
            if parent and parent.type == "call_expression":
                arguments_node = parent.child_by_field_name("arguments")
                if arguments_node and arguments_node.named_children:
                    first_arg = arguments_node.named_children[0]
                    if first_arg.type == "string":
                        package_name = first_arg.text.decode("utf-8")[1:-1]

        if not package_name:
            continue

        # Ignore relative and absolute local paths.
        if package_name.startswith(("./", "../", "/", "#")):
            continue

        # Ignore Node.js built-in modules.
        normalized = package_name.removeprefix("node:")
        root_package = normalized.split("/")[0]

        if normalized in NODE_BUILTINS or root_package in NODE_BUILTINS:
            continue

        # Convert scoped packages like @scope/package to @scope/package.
        if package_name not in seen:
            seen.add(package_name)
            detected_imports.append({
                "package": package_name,
                "line": node.start_point.row + 1,
            })

    return detected_imports
