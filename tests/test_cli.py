"""Tests for CLI interface."""

import sys
from pathlib import Path

import pytest

from mini_compiler.__main__ import main


class TestCLI:
    """Test suite for command-line interface."""

    def test_validate_command_valid_file(self, tmp_path, monkeypatch, capsys):
        """Test validate command with valid source file."""
        # Create valid source file
        source_file = tmp_path / "valid.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                a = 5 ;
                print ( a ) ;
            end
        """
        )

        # Mock sys.argv
        monkeypatch.setattr(
            sys, "argv", ["mini-compiler", "validate", str(source_file)]
        )

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with 0 for success
            assert e.code == 0 or e.code is None

        # Check output
        captured = capsys.readouterr()
        assert "valid" in captured.out.lower() or "accepted" in captured.out.lower()

    def test_validate_command_invalid_file(self, tmp_path, monkeypatch, capsys):
        """Test validate command with invalid source file."""
        # Create invalid source file (missing semicolon)
        source_file = tmp_path / "invalid.src"
        source_file.write_text(
            """
            program abc;
            var a : integer
            begin
                a = 5 ;
            end
        """
        )

        # Mock sys.argv
        monkeypatch.setattr(
            sys, "argv", ["mini-compiler", "validate", str(source_file)]
        )

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with non-zero for error
            assert e.code != 0

        # Check output
        captured = capsys.readouterr()
        assert "error" in captured.out.lower() or "error" in captured.err.lower()

    def test_validate_with_semantics_flag(self, tmp_path, monkeypatch, capsys):
        """Test validate command with --semantics flag."""
        # Create file with semantic error
        source_file = tmp_path / "semantic_error.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                b = 5 ;
            end
        """
        )

        # Mock sys.argv
        monkeypatch.setattr(
            sys, "argv", ["mini-compiler", "validate", str(source_file), "--semantics"]
        )

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with error code
            assert e.code != 0

        # Check output mentions semantic error
        captured = capsys.readouterr()
        output = captured.out.lower() + captured.err.lower()
        assert "semantic" in output or "undeclared" in output or "error" in output

    def test_compile_command_python(self, tmp_path, monkeypatch, capsys):
        """Test compile command with Python output."""
        # Create valid source file
        source_file = tmp_path / "program.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                a = 42 ;
                print ( a ) ;
            end
        """
        )

        output_file = tmp_path / "output.py"

        # Mock sys.argv
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "mini-compiler",
                "compile",
                str(source_file),
                "--output",
                "python",
                "-o",
                str(output_file),
            ],
        )

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with success
            assert e.code == 0 or e.code is None

        # Check output file was created
        assert output_file.exists()

        # Check generated code
        code = output_file.read_text()
        assert "a: int" in code
        assert "a = 42" in code
        assert "print(a)" in code

    def test_validate_nonexistent_file(self, monkeypatch, capsys):
        """Test validate command with non-existent file."""
        # Mock sys.argv with non-existent file
        monkeypatch.setattr(
            sys, "argv", ["mini-compiler", "validate", "/nonexistent/file.src"]
        )

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with error
            assert e.code != 0

        # Check error message
        captured = capsys.readouterr()
        output = captured.out.lower() + captured.err.lower()
        assert "not found" in output or "error" in output

    def test_no_command_specified(self, monkeypatch, capsys):
        """Test running with no command shows help."""
        # Mock sys.argv with no command
        monkeypatch.setattr(sys, "argv", ["mini-compiler"])

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with error code
            assert e.code != 0

        # Should show help
        captured = capsys.readouterr()
        assert "usage:" in captured.out.lower() or "usage:" in captured.err.lower()

    def test_validate_verbose_mode(self, tmp_path, monkeypatch, capsys):
        """Test validate command with verbose flag."""
        source_file = tmp_path / "program.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                a = 5 ;
            end
        """
        )

        # Mock sys.argv with verbose flag
        monkeypatch.setattr(
            sys, "argv", ["mini-compiler", "validate", str(source_file), "-v"]
        )

        # Run CLI
        try:
            main()
        except SystemExit:
            pass

        # Check verbose output
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "preprocessing" in output.lower() or "parsing" in output.lower()

    def test_compile_verbose_mode(self, tmp_path, monkeypatch, capsys):
        """Test compile command with verbose flag."""
        source_file = tmp_path / "program.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                a = 42 ;
            end
        """
        )
        output_file = tmp_path / "output.py"

        # Mock sys.argv with verbose flag
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "mini-compiler",
                "compile",
                str(source_file),
                "--output",
                "python",
                "-o",
                str(output_file),
                "-v",
            ],
        )

        # Run CLI
        try:
            main()
        except SystemExit:
            pass

        # Check verbose output
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert (
            "preprocessing" in output.lower()
            or "parsing" in output.lower()
            or "generating" in output.lower()
        )

    def test_compile_without_output_flag(self, tmp_path, monkeypatch, capsys):
        """Test compile command prints to stdout when no -o specified."""
        source_file = tmp_path / "program.src"
        source_file.write_text(
            """
            program abc;
            var a : integer ;
            begin
                a = 10 ;
            end
        """
        )

        # Mock sys.argv without -o flag
        monkeypatch.setattr(
            sys,
            "argv",
            ["mini-compiler", "compile", str(source_file), "--output", "python"],
        )

        # Run CLI
        try:
            main()
        except SystemExit:
            pass

        # Check stdout has generated code
        captured = capsys.readouterr()
        assert "a: int" in captured.out
        assert "a = 10" in captured.out
