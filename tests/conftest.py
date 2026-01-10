"""Shared pytest fixtures for mini_compiler tests.

This module provides common fixtures used across multiple test files.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mini_compiler.core.language import Language
from mini_compiler.core.preprocessor import Preprocessor
from mini_compiler.utils.constants import PARSING_TABLE, RESERVED_WORDS, SYMBOL_INDICES


@pytest.fixture
def language():
    """Create a Language instance for testing."""
    return Language("Program", PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)


@pytest.fixture
def preprocessor():
    """Create a Preprocessor instance for testing."""
    return Preprocessor()


@pytest.fixture
def simple_valid_tokens():
    """Return tokens for a simple valid program."""
    return [
        "program",
        "abc",
        ";",
        "var",
        "a",
        ":",
        "integer",
        ";",
        "begin",
        "a",
        "=",
        "5",
        ";",
        "print",
        "(",
        "a",
        ")",
        ";",
        "end",
    ]


@pytest.fixture
def complex_valid_tokens():
    """Return tokens for a program with complex expressions."""
    return [
        "program",
        "f2024",
        ";",
        "var",
        "a",
        ",",
        "b2a",
        ",",
        "c",
        ",",
        "bba",
        ":",
        "integer",
        ";",
        "begin",
        "a",
        "=",
        "33",
        ";",
        "b2a",
        "=",
        "14",
        ";",
        "c",
        "=",
        "5",
        ";",
        "print",
        "(",
        "c",
        ")",
        ";",
        "bba",
        "=",
        "(",
        "b2a",
        "+",
        "2",
        "*",
        "c",
        ")",
        "*",
        "a",
        ";",
        "print",
        "(",
        '"value=",',
        "bba",
        ")",
        ";",
        "end",
    ]


@pytest.fixture
def invalid_syntax_tokens():
    """Return tokens with syntax error (missing semicolon)."""
    return [
        "program",
        "bad",
        ";",
        "var",
        "a",
        ":",
        "integer",
        ";",
        "begin",
        "a",
        "=",
        "5",  # Missing semicolon
        "print",
        "(",
        "a",
        ")",
        ";",
        "end",
    ]


@pytest.fixture
def undeclared_var_tokens():
    """Return tokens with undeclared variable."""
    return [
        "program",
        "bad",
        ";",
        "var",
        "a",
        ":",
        "integer",
        ";",
        "begin",
        "a",
        "=",
        "5",
        ";",
        "b",
        "=",
        "10",
        ";",  # 'b' not declared
        "print",
        "(",
        "b",
        ")",
        ";",
        "end",
    ]
