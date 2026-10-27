# DepShield 

### Automated Slopsquatting and Dependency Hallucination Detection and Defense using AI

DepShield is a software supply-chain security project designed to identify suspicious, hallucinated, and potentially risky dependencies in source code. It aims to help developers detect dependency-related risks introduced through manual coding or AI-generated code before they become security problems.

## Problem Statement

AI coding assistants can occasionally suggest package names that do not exist or that resemble legitimate packages. Attackers may exploit this behavior through **slopsquatting** by publishing malicious packages under names that AI tools are likely to hallucinate.

Traditional dependency checks may not identify every suspicious package name. DepShield aims to address this gap by extracting dependencies from source code and checking them against package registry information.

## Key Features

- **Python AST Parser:** Extracts external imports using Python's built-in Abstract Syntax Tree module.
- **JavaScript/TypeScript Parser:** Uses Tree-sitter to identify package imports in JavaScript and TypeScript source files.
- **Source-Line Tracking:** Records the line number associated with each detected dependency.
- **Import Filtering:** Excludes Python standard-library modules and common JavaScript built-in modules and local imports.
- **Duplicate Handling:** Deduplicates package names within a parsed file.
- **Unit Testing:** Tests parser behavior, dependency extraction, filtering, and invalid Python syntax handling.
- **Extensible Architecture:** Separates parsing from dependency verification to support further development.

## Architecture

DepShield is being developed as a modular dependency-scanning system.

```text
             Source Code
                  |
                  v
          Language Detection
                  |
          +-------+-------+
          |               |
          v               v
     Python Parser    JS/TS Parser
       (Python AST)   (Tree-sitter)
          |               |
          +-------+-------+
                  |
                  v
       Extracted Dependencies
       Package Name + Line No.
                  |
                  v
       Registry Verification
                  |
                  v
        Risk Analysis
                  |
                  v
          Scan Report
```

The parser modules form the source-analysis layer. The complete workflow depends on integrating them with the verification, analysis, and reporting components.

## Tech Stack

| Component | Technology |
|---|---|
| Python source parsing | Python AST |
| JavaScript/TypeScript parsing | Tree-sitter |
| Programming languages | Python, JavaScript, TypeScript |
| Dependency verification | Package registry APIs |
| Automated testing | Python `unittest` |
| Version control | Git and GitHub |

## Project Structure

```text
DepShield/
├── engine/
│   ├── parser/
│   │   ├── py_parser.py
│   │   └── js_parser.py
│   ├── verifier/
│   │   ├── registry_api.py
│   │   └── cache.py
│   └── main.py
├── tests/
│   ├── test_py_parser.py
│   └── test_js_parser.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: This structure represents the intended core modules; files and integration status may vary as development progresses.*

## Getting Started

### Prerequisites

- Python 3.10 or later recommended
- Git
- Internet access for installing dependencies and accessing package registries

### 1. Clone the repository

```bash
git clone https://github.com/DepShield-Team/DepShield.git
cd DepShield
```

### 2. Create and activate a virtual environment

**Windows — Command Prompt**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install parser dependencies

Install the dependencies listed in the project's shared requirements file:

```bash
python -m pip install -r requirements.txt
```

The JavaScript/TypeScript parser requires these packages:

```bash
python -m pip install tree-sitter tree-sitter-javascript tree-sitter-typescript
```

## Running Tests

From the repository root, execute:

```bash
python -m unittest discover -s tests -v
```

The parser unit tests cover:

- Extracting external imports from Python files.
- Detecting imports inside Python functions.
- Handling invalid Python syntax.
- Extracting JavaScript imports, `require()` calls, and dynamic imports.
- Filtering local imports and common built-in modules.
- Extracting dependencies from TypeScript files.

The parser tests previously passed with **5 tests**. Run the command above on the latest `main` branch to verify the current test status.

## Example: Dependency Extraction

Given a Python source file:

```python
import requests
import suspicious_package
```

The parser returns dependency information in this format:

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

The extracted package names can then be passed to the verification layer for further analysis.

**Important:** Extracting a package name does not establish that it is malicious. Registry availability, package metadata, naming similarity, and other evidence must be considered before determining risk.

## Why DepShield?

- Helps investigate suspicious dependency names.
- Supports dependency extraction across multiple programming languages.
- Preserves source-line information for easier debugging.
- Separates source parsing from verification logic.
- Provides a foundation for detecting dependency hallucinations and potential slopsquatting attacks.
- Can be extended with additional languages, registries, and security checks.

## Future Scope

Potential enhancements include:

- Integrating parsers with a unified scanning entry point.
- Verifying packages against supported registries.
- Detecting suspicious package names and potential typosquatting.
- Improving package metadata analysis and risk classification.
- Adding caching to reduce repeated registry requests.
- Generating detailed terminal reports.
- Integrating with CI/CD workflows.
- Developing a dashboard for viewing scan results.

## Contributing

DepShield is developed collaboratively using Git and GitHub.

1. Create a feature branch for your task.
2. Implement the change and add relevant tests.
3. Run the test suite before submitting changes.
4. Open a pull request with a clear summary.
5. Coordinate with the team when changing shared interfaces or dependencies.

## Team

**DepShield Team**

Repository: [github.com/DepShield-Team/DepShield](https://github.com/DepShield-Team/DepShield)

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to the terms and conditions of the MIT License.

---

*DepShield — Helping developers identify suspicious dependencies before they become a supply-chain security risk.*
