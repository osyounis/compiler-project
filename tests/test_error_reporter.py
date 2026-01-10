"""Tests for the ErrorReporter class."""

import pytest
from mini_compiler.errors.error_reporter import ErrorReporter, CompilationError, ErrorType


class TestErrorReporter:
    """Test suite for ErrorReporter class."""
    
    def test_initialization(self):
        """Test ErrorReporter initializes empty."""
        reporter = ErrorReporter()
        
        assert not reporter.has_errors()
        assert reporter.error_count() == 0
    
    def test_add_error(self):
        """Test adding an error."""
        reporter = ErrorReporter()
        error = CompilationError(ErrorType.SYNTAX, "Test error")
        
        reporter.add_error(error)
        
        assert reporter.has_errors()
        assert reporter.error_count() == 1
    
    def test_get_errors(self):
        """Test getting all errors."""
        reporter = ErrorReporter()
        error1 = CompilationError(ErrorType.SYNTAX, "Error 1")
        error2 = CompilationError(ErrorType.SEMANTIC, "Error 2")
        
        reporter.add_error(error1)
        reporter.add_error(error2)
        
        errors = reporter.get_errors()
        assert len(errors) == 2
    
    def test_clear_errors(self):
        """Test clearing all errors."""
        reporter = ErrorReporter()
        reporter.add_error(CompilationError(ErrorType.SYNTAX, "Test"))
        
        assert reporter.has_errors()
        
        reporter.clear()
        
        assert not reporter.has_errors()
        assert reporter.error_count() == 0
    
    def test_check_variable_declared_valid(self):
        """Test checking declared variable."""
        reporter = ErrorReporter()
        declared = {'a', 'b', 'c'}
        
        result = reporter.check_variable_declared('a', declared, line=5)
        
        assert result is True
        assert not reporter.has_errors()
    
    def test_check_variable_declared_invalid(self):
        """Test checking undeclared variable."""
        reporter = ErrorReporter()
        declared = {'a', 'b', 'c'}
        
        result = reporter.check_variable_declared('x', declared, line=5)
        
        assert result is False
        assert reporter.has_errors()
        assert reporter.error_count() == 1
    
    def test_check_variable_not_redeclared_valid(self):
        """Test checking variable is not already declared."""
        reporter = ErrorReporter()
        declared = {'a', 'b'}
        
        result = reporter.check_variable_not_redeclared('c', declared, line=3)
        
        assert result is True
        assert not reporter.has_errors()
    
    def test_check_variable_not_redeclared_invalid(self):
        """Test detecting redeclaration."""
        reporter = ErrorReporter()
        declared = {'a', 'b'}
        
        result = reporter.check_variable_not_redeclared('a', declared, line=3)
        
        assert result is False
        assert reporter.has_errors()
    
    def test_add_syntax_error(self):
        """Test convenience method for adding syntax errors."""
        reporter = ErrorReporter()
        
        reporter.add_syntax_error("Missing semicolon", line=5, column=10, token=';')
        
        assert reporter.has_errors()
        errors = reporter.get_errors()
        assert errors[0].error_type == ErrorType.SYNTAX
    
    def test_add_semantic_error(self):
        """Test convenience method for adding semantic errors."""
        reporter = ErrorReporter()
        
        reporter.add_semantic_error("Undeclared variable 'x'", line=8, token='x')
        
        assert reporter.has_errors()
        errors = reporter.get_errors()
        assert errors[0].error_type == ErrorType.SEMANTIC
    
    def test_get_error_summary(self):
        """Test getting error summary string."""
        reporter = ErrorReporter()
        reporter.add_syntax_error("Error 1", line=5)
        reporter.add_semantic_error("Error 2", line=8)
        
        summary = reporter.get_error_summary()
        
        assert 'Error 1' in summary
        assert 'Error 2' in summary
        assert 'line 5' in summary
        assert 'line 8' in summary


class TestCompilationError:
    """Test suite for CompilationError class."""
    
    def test_error_string_with_line(self):
        """Test error string formatting with line number."""
        error = CompilationError(ErrorType.SYNTAX, "Test error", line=5)
        error_str = str(error)
        
        assert 'Syntax Error' in error_str
        assert 'line 5' in error_str
        assert 'Test error' in error_str
    
    def test_error_string_with_line_and_column(self):
        """Test error string formatting with line and column."""
        error = CompilationError(ErrorType.SYNTAX, "Test error", line=5, column=10)
        error_str = str(error)
        
        assert 'line 5' in error_str
        assert 'column 10' in error_str
    
    def test_error_string_with_token(self):
        """Test error string formatting with token info."""
        error = CompilationError(ErrorType.SEMANTIC, "Undeclared", token='foo')
        error_str = str(error)
        
        assert "token: 'foo'" in error_str
