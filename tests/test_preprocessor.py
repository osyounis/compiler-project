"""Tests for the Preprocessor class."""

from pathlib import Path

import pytest

from mini_compiler.core.preprocessor import Preprocessor


class TestPreprocessor:
    """Test suite for Preprocessor class."""

    def test_process_string_basic(self, preprocessor):
        """Test basic string processing."""
        source = "program abc; var a : integer ;"
        tokens = preprocessor.process_string(source)

        assert tokens == ["program", "abc;", "var", "a", ":", "integer", ";"]

    def test_comment_removal(self, preprocessor):
        """Test that comments are properly removed."""
        source = "program abc; (* this is a comment *) var a : integer ;"
        tokens = preprocessor.process_string(source)

        assert "(*" not in tokens
        assert "comment" not in tokens
        assert "*)" not in tokens
        assert tokens == ["program", "abc;", "var", "a", ":", "integer", ";"]

    def test_multiline_comment_removal(self, preprocessor):
        """Test removal of multiline comments."""
        source = """program abc;
        (* this comment
           spans multiple
           lines *)
        var a : integer ;"""
        tokens = preprocessor.process_string(source)

        assert "comment" not in tokens
        assert "spans" not in tokens
        assert "lines" not in tokens

    def test_whitespace_normalization(self, preprocessor):
        """Test that multiple spaces are normalized to single space."""
        source = "program    abc;    var     a   :   integer  ;"
        tokens = preprocessor.process_string(source)

        # Should be same as if there were single spaces
        expected = preprocessor.process_string("program abc; var a : integer ;")
        assert tokens == expected

    def test_case_insensitive_tokenization(self, preprocessor):
        """Test that all tokens are converted to lowercase."""
        source = "Program ABC; Var A : Integer ;"
        tokens = preprocessor.process_string(source)

        assert all(token == token.lower() or not token.isalpha() for token in tokens)
        assert "program" in tokens
        assert "var" in tokens
        assert "integer" in tokens
        assert "ABC" not in tokens  # Should be lowercase

    def test_mixed_case_identifier(self, preprocessor):
        """Test that mixed-case identifiers are lowercased."""
        source = "program ABC; var A, B, C : integer ;"
        tokens = preprocessor.process_string(source)

        assert "abc;" in tokens
        assert "a," in tokens or "a" in tokens  # depending on tokenization
        assert "ABC" not in "".join(tokens)

    def test_empty_lines_removed(self, preprocessor):
        """Test that empty lines are removed."""
        source = """program abc;

        var a : integer ;

        begin

        end"""
        tokens = preprocessor.process_string(source)

        # Should have content, no empty strings
        assert all(token for token in tokens)
        assert "" not in tokens

    def test_process_file_valid(self, preprocessor, tmp_path):
        """Test processing a valid source file."""
        # Create temporary source file
        source_file = tmp_path / "abc.src"
        source_file.write_text("program abc; var a : integer ;")

        tokens = preprocessor.process_file(str(source_file))

        assert len(tokens) > 0
        assert "program" in tokens

    def test_process_file_not_found(self, preprocessor):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError) as exc_info:
            preprocessor.process_file("/nonexistent/file.src")

        assert "not found" in str(exc_info.value).lower()

    def test_process_file_permission_error(self, preprocessor, tmp_path):
        """Test handling of permission/IO errors."""
        import os

        # Create a file and make it unreadable (Unix only)
        if os.name != "nt":  # Skip on Windows
            source_file = tmp_path / "unreadable.src"
            source_file.write_text("program abc;")
            source_file.chmod(0o000)  # Remove all permissions

            try:
                with pytest.raises(IOError):
                    preprocessor.process_file(str(source_file))
            finally:
                # Restore permissions for cleanup
                source_file.chmod(0o644)

    def test_save_preprocessed(self, preprocessor, tmp_path):
        """Test saving preprocessed output to file."""
        source_file = tmp_path / "input.src"
        output_file = tmp_path / "output.txt"

        source_file.write_text("program abc; (* comment *) var a : integer ;")

        preprocessor.save_preprocessed(str(source_file), str(output_file))

        # Check output file was created
        assert output_file.exists()

        # Check comment was removed
        content = output_file.read_text()
        assert "comment" not in content

    def test_complex_expression_tokenization(self, preprocessor):
        """Test tokenization of complex expressions."""
        source = "a = ( b + 2 * c ) * d ;"
        tokens = preprocessor.process_string(source)

        # Should preserve all operators and parentheses
        assert "(" in tokens
        assert ")" in tokens
        assert "+" in tokens or "+" in "".join(tokens)
        assert "*" in tokens or "*" in "".join(tokens)

    def test_nested_comments(self, preprocessor):
        """Test that nested comments are handled.

        Note: True nested comment support requires a parser. The regex-based
        approach handles simple cases but may not properly handle all nesting.
        """
        source = "program abc; (* comment one *) var a : integer ; (* comment two *)"
        tokens = preprocessor.process_string(source)

        # Both comments should be removed
        assert "comment" not in tokens
        assert "one" not in tokens
        assert "two" not in tokens
