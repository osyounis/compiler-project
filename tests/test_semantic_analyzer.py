"""Tests for the SemanticAnalyzer class."""

import pytest

from mini_compiler.core.semantic_analyzer import SemanticAnalyzer


class TestSemanticAnalyzer:
    """Test suite for SemanticAnalyzer class."""

    def test_analyze_valid_program(self, simple_valid_tokens):
        """Test semantic analysis on valid program."""
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(simple_valid_tokens)

        assert not errors.has_errors()
        assert errors.error_count() == 0

    def test_detect_undeclared_variable(self, undeclared_var_tokens):
        """Test detection of undeclared variable usage."""
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(undeclared_var_tokens)

        assert errors.has_errors()
        assert errors.error_count() >= 1

        # Check error mentions the undeclared variable
        error_messages = [str(e) for e in errors.get_errors()]
        assert any("b" in msg.lower() for msg in error_messages)

    def test_extract_declarations(self, complex_valid_tokens):
        """Test that declarations are correctly extracted."""
        analyzer = SemanticAnalyzer()
        declared = analyzer._extract_declarations(complex_valid_tokens)

        assert "a" in declared
        assert "b2a" in declared
        assert "c" in declared
        assert "bba" in declared

    def test_no_declarations(self):
        """Test program with no var section."""
        tokens = ["program", "abc", ";", "begin", "end"]
        analyzer = SemanticAnalyzer()
        declared = analyzer._extract_declarations(tokens)

        assert len(declared) == 0

    def test_multiple_undeclared_variables(self):
        """Test detection of multiple undeclared variables."""
        tokens = [
            "program",
            "abc",
            ";",
            "var",
            "a",
            ":",
            "integer",
            ";",
            "begin",
            "b",
            "=",
            "5",
            ";",  # undeclared
            "c",
            "=",
            "10",
            ";",  # undeclared
            "end",
        ]
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(tokens)

        # Should detect both 'b' and 'c'
        assert errors.error_count() >= 2
