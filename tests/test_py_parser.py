
import tempfile
import unittest
from pathlib import Path

from engine.parser.py_parser import extract_python_imports


class TestPythonParser(unittest.TestCase):

    def test_extracts_external_imports(self):
        source = """
import os
import requests
from flask import Flask
import requests.sessions
"""

        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "sample.py"
            file_path.write_text(source, encoding="utf-8")
            result = extract_python_imports(str(file_path))

        self.assertEqual(
            [item["package"] for item in result],
            ["requests", "flask"]
        )

    def test_extracts_import_inside_function(self):
        source = """
def load():
    import pandas
"""

        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "sample.py"
            file_path.write_text(source, encoding="utf-8")
            result = extract_python_imports(str(file_path))

        self.assertEqual(result[0]["package"], "pandas")
        self.assertEqual(result[0]["line"], 3)

    def test_invalid_syntax_raises_error(self):
        source = "def broken(:"

        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "sample.py"
            file_path.write_text(source, encoding="utf-8")

            with self.assertRaises(SyntaxError):
                extract_python_imports(str(file_path))


if __name__ == "__main__":
    unittest.main()
