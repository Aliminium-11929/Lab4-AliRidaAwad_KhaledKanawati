"""Sphinx configuration for the Lab 3 project documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "School Management System"
author = "Khaled Kanawati"
copyright = "2026, Khaled Kanawati"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

autodoc_mock_imports = ["PyQt5"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
templates_path = []
html_theme = "sphinx_rtd_theme"
html_static_path = []
