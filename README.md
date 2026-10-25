# DepShield 

**Automated Slopsquatting and Dependency Hallucination Detection and Defense using AI**

DepShield is a security-focused project designed to identify potentially hallucinated, misspelled, or suspicious software dependencies in source code. It extracts package dependencies from Python and JavaScript/TypeScript files and aims to verify them against package registries to help developers identify potentially risky dependencies before they enter a project.

## Problem Statement

Modern software development relies heavily on third-party packages. However, developers and AI coding assistants can introduce incorrect or non-existent package names into source code.

Attackers can exploit this behavior through **slopsquatting**—publishing malicious packages with names that developers or AI tools are likely to hallucinate.

DepShield aims to address this risk by automatically extracting dependencies, checking their availability, and reporting potentially suspicious packages.

## Key Features

- **Python AST Parsing:** Extracts external package imports from Python source files using Python's Abstract Syntax Tree (AST).
- **JavaScript/TypeScript Parsing:** Uses Tree-sitter to analyze JavaScript and TypeScript source files.
- **Dependency Extraction:** Identifies imported packages and records their source line numbers.
- **Import Filtering:** Excludes Python standard-library modules and common JavaScript local imports and built-in modules.
- **Registry Verification:** Designed to check extracted package names against package registry information.
- **Risk Reporting:** Aims to present dependency verification results in an understandable report.
- **Automated Testing:** Includes unit tests for parser behavior and error handling.

*Note: Registry verification, risk reporting, caching, and dashboard functionality depend on their respective modules and integration status.*

## Project Architecture

```text
DepShield/
├── engine/
│   ├── parser/
│   │   ├── py_parser.py       # Python AST parser
│   │   └── js_parser.py       # JavaScript/TypeScript parser
│   ├── verifier/
│   │   ├── registry_api.py    # Package registry verification
│   │   └── cache.py           # Verification caching
│   └── main.py                # Scanner entry point
├── tests/
│   ├── test_py_parser.py      # Python parser tests
│   └── test_js_parser.py      # JavaScript/TypeScript parser tests
├── requirements.txt
├── .gitignore
└── README.md
```

The repository structure may evolve as the scanner, verification engine, and user interface are integrated.

## Technology Stack

| Component | Technology |
|---|---|
| Python parsing | Python `ast` module |
| JavaScript/TypeScript parsing | Tree-sitter |
| Dependency verification | Package registry APIs |
| Testing | Python `unittest` |
| Version control | Git and GitHub |

## Getting Started

### Prerequisites

- Python 3.10 or later recommended
- Git
- Internet access for package installation and registry verification

### 1. Clone the repository

```bash
git clone https://github.com/DepShield-Team/DepShield.git
cd DepShield
```

### 2. Create a virtual environment

**Windows (Command Prompt):**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The parser dependencies include:

- `tree-sitter`
- `tree-sitter-javascript`
- `tree-sitter-typescript`

Ensure these packages are listed in `requirements.txt` before running the JavaScript/TypeScript parser.

## Running Tests

Run the parser unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The parser tests cover scenarios such as:

- Extracting external imports from Python files.
- Detecting imports inside functions.
- Handling invalid Python syntax.
- Extracting JavaScript imports, `require()` calls, and dynamic imports.
- Ignoring local imports and common built-in modules.
- Extracting package names from TypeScript source files.

## How It Works

DepShield follows a dependency-scanning workflow:

1. **Source Input:** A source file is provided for analysis.
2. **Language Detection:** The appropriate parser is selected for the file type.
3. **Dependency Extraction:** The parser identifies external dependencies and their line numbers.
4. **Registry Verification:** Extracted package names are checked against supported package registry data.
5. **Risk Analysis:** Verification results are used to identify dependencies that may require further investigation.
6. **Report Generation:** Findings are presented to help developers review suspicious dependencies.

The complete workflow depends on integration between the parsers, verification modules, and scanner entry point.

## Example Parser Output

For a source file containing:

```python
import requests
import suspicious_package
```

The parser returns a list of detected dependencies in the following format:

```json
[
  {
    "package": "requests",
    "line": 1
  },
  {
    "package": "suspicious_package",
    "line": 2
  }
]
```

This output provides the package name and the line where the import occurs, allowing later stages to verify the dependency and report findings.

## Why DepShield?

- Helps identify potentially unsafe dependency names early in development.
- Supports multiple programming languages.
- Provides source-line information to simplify investigation.
- Separates dependency extraction from registry verification.
- Can be extended to support additional languages, registries, and risk-analysis techniques.

**Important:** A package missing from a registry is not automatically malicious, and a package existing in a registry does not guarantee that it is safe. Findings should be treated as signals for further investigation.

## Future Scope

Potential improvements include:

- More comprehensive dependency and package-name risk analysis.
- Improved handling of aliases, scoped packages, and edge cases.
- Support for additional programming languages and package registries.
- Better caching and performance for repeated scans.
- Richer terminal reports and dashboard visualizations.
- Integration into CI/CD pipelines to flag suspicious dependencies during development.

## Contributing

DepShield is developed collaboratively.

1. Fork or clone the repository.
2. Create a feature branch.
3. Implement your changes and add relevant tests.
4. Run the test suite.
5. Submit a pull request with a clear description of the changes.

Please coordinate with the team before changing shared interfaces between the parser, verifier, and scanner.

## Team

**DepShield Team** — collaborative development project.

## License

A license has not yet been specified. Until one is added to the repository, reuse and redistribution are subject to applicable copyright restrictions.

---

*DepShield — Detect suspicious dependencies before they become a security problem.*
