
import tempfile
import unittest
from pathlib import Path

from engine.parser.js_parser import extract_javascript_imports


class TestJavaScriptParser(unittest.TestCase):

    def test_extracts_import_and_require(self):
        source = '''
import React from "react";
import { useState } from "react";
const axios = require("axios");
import("lodash");
import "./styles.css";
const fs = require("fs");
'''

        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "sample.js"
            file_path.write_text(source, encoding="utf-8")
            result = extract_javascript_imports(str(file_path))

        packages = [item["package"] for item in result]
        self.assertEqual(packages, ["react", "axios", "lodash"])
        # Static and dynamic import syntax may have different AST representations.

    def test_extracts_typescript_package(self):
        source = 'import type { User } from "@types/node";'

        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "sample.ts"
            file_path.write_text(source, encoding="utf-8")
            result = extract_javascript_imports(str(file_path))

        self.assertEqual(result[0]["package"], "@types/node")


if __name__ == "__main__":
    unittest.main()
