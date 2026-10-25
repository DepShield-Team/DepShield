import os
import re
import subprocess


def get_pr_modified_lines(base_ref: str = "origin/main") -> dict[str, set[int]]:
    """
    Executes 'git diff origin/main...HEAD -U0' to isolate only the exact lines
    added or modified in the current pull request.
    Returns a mapping of {file_path: {line_numbers}}.
    Example: {"app.py": {3, 4, 15}, "src/index.js": {1, 2}}
    """
    try:
        cmd = ["git", "diff", f"{base_ref}...HEAD", "-U0"]
        diff_output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        # Fallback for shallow checkouts or detached HEADs
        try:
            cmd = ["git", "diff", "HEAD~1...HEAD", "-U0"]
            diff_output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        except Exception:
            return {}

    modified_lines: dict[str, set[int]] = {}
    current_file = None

    for line in diff_output.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            continue

        if not current_file:
            continue

        # Match chunk header: @@ -old_start,count +new_start,count @@
        match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if match:
            start = int(match.group(1))
            count = int(match.group(2)) if match.group(2) is not None else 1

            if current_file not in modified_lines:
                modified_lines[current_file] = set()

            for line_no in range(start, start + count):
                modified_lines[current_file].add(line_no)

    return modified_lines


if __name__ == "__main__":
    changes = get_pr_modified_lines()
    print("Detected changed files and line numbers:")
    for file, lines in changes.items():
        print(f"  {file}: lines {sorted(list(lines))}")