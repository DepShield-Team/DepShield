import asyncio
import json
import os
import sys
import urllib.request
from pathlib import Path

# Step 2: Line diff isolation
from engine.ci.git_diff import get_pr_modified_lines

# Member 2: AST parsers
try:
    from engine.parser.py_parser import extract_python_imports
except ImportError:
    extract_python_imports = None

try:
    from engine.parser.js_parser import extract_javascript_imports
except ImportError:
    extract_javascript_imports = None

# Member 3: Verification pipeline
try:
    from engine.pipeline import verify_dependencies
except ImportError:
    verify_dependencies = None


def post_github_pr_comment(token: str, repo: str, pr_number: str, comment_body: str):
    """
    Posts an automated review comment to the GitHub Pull Request
    using Python standard library (urllib.request), requiring zero extra dependencies.
    """
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DepShield-Security-Guard",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"body": comment_body}).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 201):
                print("✔ Successfully posted security comment to GitHub Pull Request.")
    except Exception as e:
        print(f"⚠️ Failed to post GitHub comment: {e}")


async def fallback_check_pypi(package_name: str) -> bool:
    """Fallback check directly against PyPI if pipeline module is loading."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    req = urllib.request.Request(url, headers={"User-Agent": "DepShield-Fallback"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        return True
    except Exception:
        return True


async def run_ci_audit():
    print("🛡️ [DepShield] Initializing automated PR Gatekeeper inspection...")

    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    # 1. Inspect PR diff lines
    modified_files = get_pr_modified_lines()
    if not modified_files:
        print("✔ No source modifications detected in this PR diff.")
        sys.exit(0)

    imports_to_verify = []

    # 2. Extract imports using Member 2's AST parsers
    for file_path, added_lines in modified_files.items():
        if not Path(file_path).exists():
            continue

        raw_imports = []
        if file_path.endswith(".py") and extract_python_imports:
            try:
                raw_imports = extract_python_imports(file_path)
            except Exception as e:
                print(f"⚠️ Python parser error on {file_path}: {e}")
        elif file_path.endswith((".js", ".jsx", ".ts", ".tsx")) and extract_javascript_imports:
            try:
                raw_imports = extract_javascript_imports(file_path)
            except Exception as e:
                print(f"⚠️ JS/TS parser error on {file_path}: {e}")

        for item in raw_imports:
            if item["line"] in added_lines:
                imports_to_verify.append({
                    "package": item["package"],
                    "line": item["line"],
                    "file": file_path,
                })

    if not imports_to_verify:
        print("✔ No new third-party dependency imports introduced in this PR.")
        sys.exit(0)

    print(f"🔍 Inspecting {len(imports_to_verify)} newly introduced import statements...")

    # 3. Verify via Member 3's pipeline or fallback check
    critical_findings = []

    if verify_dependencies:
        results = await verify_dependencies(imports_to_verify)
        for res in results:
            if res.get("status") in {"NOT_FOUND", "CRITICAL"}:
                critical_findings.append({
                    "file": res.get("file", "unknown"),
                    "line": res.get("line", "?"),
                    "package": res.get("package"),
                    "reason": "404 Not Found on public registry (Hallucinated dependency / Slopsquat target).",
                })
    else:
        # Fallback check
        for item in imports_to_verify:
            exists = await fallback_check_pypi(item["package"])
            if not exists:
                critical_findings.append({
                    "file": item["file"],
                    "line": item["line"],
                    "package": item["package"],
                    "reason": "404 Not Found on PyPI (Hallucinated package).",
                })

    # 4. Enforce security block on failures
    if critical_findings:
        print("\n" + "=" * 75)
        print("🚨 [DepShield Alert] Non-existent / Hallucinated Dependencies Detected:")
        for finding in critical_findings:
            print(f"  • {finding['file']}:{finding['line']} -> {finding['package']}")
        print("=" * 75)

        # Post review comment to GitHub PR
        if github_token and repo_name and pr_number:
            rows = "\n".join([
                f"| `{f['file']}` | Line {f['line']} | `{f['package']}` | **CRITICAL (404)** | {f['reason']} |"
                for f in critical_findings
            ])
            comment_markdown = (
                "### 🛡️ DepShield Security Alert: PR Blocked\n\n"
                "DepShield detected unverified or hallucinated dependencies introduced in this pull request.\n\n"
                "| File | Line | Dependency | Threat Status | Details |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
                f"{rows}\n\n"
                "> **Remedy Required:** Remove the phantom import or register/replace it with an authentic library before merging.\n"
            )
            post_github_pr_comment(github_token, repo_name, pr_number, comment_markdown)

        # Non-zero exit code blocks the GitHub PR merge button
        print("\n❌ CI Check Failed: PR blocked to prevent slopsquatting.")
        sys.exit(1)

    print("\n✔ [DepShield Passed] All added dependencies verified successfully.")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(run_ci_audit())