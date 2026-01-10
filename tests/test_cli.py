"""Tests for CLI interface."""

import pytest
from pathlib import Path
import sys
from mini_compiler.__main__ import main


class TestCLI:
    """Test suite for command-line interface."""

    def test_validate_command_valid_file(self, tmp_path, monkeypatch, capsys):
        """Test validate command with valid source file."""
        # Create valid source file
        source_file = tmp_path / "valid.src"
        source_file.write_text("""
            program abc;
            var a : integer ;
            begin
                a = 5 ;
                print ( a ) ;
            end
        """)

        # Mock sys.argv
        monkeypatch.setattr(sys, 'argv', ['mini-compiler', 'validate', str(source_file)])

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with 0 for success
            assert e.code == 0 or e.code is None

        # Check output
        captured = capsys.readouterr()
        assert 'valid' in captured.out.lower() or 'accepted' in captured.out.lower()

    def test_validate_command_invalid_file(self, tmp_path, monkeypatch, capsys):
        """Test validate command with invalid source file."""
        # Create invalid source file (missing semicolon)
        source_file = tmp_path / "invalid.src"
        source_file.write_text("""
            program abc;
            var a : integer
            begin
                a = 5 ;
            end
        """)

        # Mock sys.argv
        monkeypatch.setattr(sys, 'argv', ['mini-compiler', 'validate', str(source_file)])

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with non-zero for error
            assert e.code != 0

        # Check output
        captured = capsys.readouterr()
        assert 'error' in captured.out.lower() or 'error' in captured.err.lower()

    def test_validate_with_semantics_flag(self, tmp_path, monkeypatch, capsys):
        """Test validate command with --semantics flag."""
        # Create file with semantic error
        source_file = tmp_path / "semantic_error.src"
        source_file.write_text("""
            program abc;
            var a : integer ;
            begin
                b = 5 ;
            end
        """)

        # Mock sys.argv
        monkeypatch.setattr(sys, 'argv', ['mini-compiler', 'validate', str(source_file), '--semantics'])

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with error code
            assert e.code != 0

        # Check output mentions semantic error
        captured = capsys.readouterr()
        output = captured.out.lower() + captured.err.lower()
        assert 'semantic' in output or 'undeclared' in output or 'error' in output

    def test_compile_command_python(self, tmp_path, monkeypatch, capsys):
        """Test compile command with Python output."""
        # Create valid source file
        source_file = tmp_path / "program.src"
        source_file.write_text("""
            program abc;
            var a : integer ;
            begin
                a = 42 ;
                print ( a ) ;
            end
        """)

        output_file = tmp_path / "output.py"

        # Mock sys.argv
        monkeypatch.setattr(sys, 'argv', [
            'mini-compiler', 'compile', str(source_file),
            '--output', 'python',
            '-o', str(output_file)
        ])

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
        assert 'a: int' in code
        assert 'a = 42' in code
        assert 'print(a)' in code

    def test_validate_nonexistent_file(self, monkeypatch, capsys):
        """Test validate command with non-existent file."""
        # Mock sys.argv with non-existent file
        monkeypatch.setattr(sys, 'argv', ['mini-compiler', 'validate', '/nonexistent/file.src'])

        # Run CLI
        try:
            main()
        except SystemExit as e:
            # Should exit with error
            assert e.code != 0

        # Check error message
        captured = capsys.readouterr()
        output = captured.out.lower() + captured.err.lower()
        assert 'not found' in output or 'error' in output
