"""Tests for the Parser class."""

import pytest
from mini_compiler.core.parser import Parser, ParseResult


class TestParser:
    """Test suite for Parser class."""
    
    def test_parse_simple_valid_program(self, language, simple_valid_tokens):
        """Test parsing a simple valid program."""
        parser = Parser(language, simple_valid_tokens)
        result = parser.parse()
        
        assert result.accepted is True
        assert result.error_message is None
    
    def test_parse_complex_valid_program(self, language, complex_valid_tokens):
        """Test parsing a program with complex expressions."""
        parser = Parser(language, complex_valid_tokens)
        result = parser.parse()
        
        assert result.accepted is True
        assert result.error_message is None
    
    def test_parse_invalid_syntax(self, language, invalid_syntax_tokens):
        """Test that syntax errors are detected."""
        parser = Parser(language, invalid_syntax_tokens)
        result = parser.parse()
        
        assert result.accepted is False
        assert result.error_message is not None
        assert 'error' in result.error_message.lower() or 'unexpected' in result.error_message.lower()
    
    def test_parse_empty_input(self, language):
        """Test parsing empty token list."""
        parser = Parser(language, [])
        result = parser.parse()
        
        assert result.accepted is False
        assert result.error_message is not None
        assert 'empty' in result.error_message.lower()
    
    def test_parse_result_attributes(self, language, simple_valid_tokens):
        """Test that ParseResult has correct attributes."""
        parser = Parser(language, simple_valid_tokens)
        result = parser.parse()
        
        assert hasattr(result, 'accepted')
        assert hasattr(result, 'error_message')
        assert hasattr(result, 'position')
        assert hasattr(result, 'semantic_errors')
    
    def test_parse_with_semantics_valid(self, language, simple_valid_tokens):
        """Test parse_with_semantics on valid program."""
        parser = Parser(language, simple_valid_tokens)
        result = parser.parse_with_semantics()
        
        assert result.accepted is True
        assert not result.semantic_errors.has_errors()
    
    def test_parse_with_semantics_undeclared_var(self, language, undeclared_var_tokens):
        """Test parse_with_semantics detects undeclared variables."""
        parser = Parser(language, undeclared_var_tokens)
        result = parser.parse_with_semantics()
        
        # Syntax should be valid
        assert result.accepted is True
        
        # But semantic errors should exist
        assert result.semantic_errors.has_errors()
        assert result.semantic_errors.error_count() > 0
    
    def test_parse_with_ast_valid(self, language, simple_valid_tokens):
        """Test parse_with_ast on valid program."""
        parser = Parser(language, simple_valid_tokens)
        result = parser.parse_with_ast()
        
        assert result.accepted is True
        assert result.ast is not None
        assert hasattr(result.ast, 'name')
        assert hasattr(result.ast, 'declarations')
        assert hasattr(result.ast, 'statements')
    
    def test_parse_with_ast_invalid(self, language, invalid_syntax_tokens):
        """Test parse_with_ast on invalid program."""
        parser = Parser(language, invalid_syntax_tokens)
        result = parser.parse_with_ast()
        
        assert result.accepted is False
        assert result.ast is None
    
    def test_parse_position_tracking(self, language, invalid_syntax_tokens):
        """Test that error position is tracked."""
        parser = Parser(language, invalid_syntax_tokens)
        result = parser.parse()
        
        assert result.accepted is False
        assert result.position is not None
        assert isinstance(result.position, int)
    
    def test_parse_multiple_variables(self, language):
        """Test parsing program with multiple variable declarations."""
        tokens = [
            'program', 'abc', ';',
            'var', 'a', ',', 'b', ',', 'c', ':', 'integer', ';',
            'begin',
            'a', '=', '1', ';',
            'end'
        ]
        parser = Parser(language, tokens)
        result = parser.parse()

        assert result.accepted is True
    
    def test_parse_arithmetic_expression(self, language):
        """Test parsing arithmetic expressions."""
        tokens = [
            'program', 'abc', ';',
            'var', 'a', ',', 'b', ',', 'c', ':', 'integer', ';',
            'begin',
            'c', '=', 'a', '+', 'b', '*', '2', ';',
            'end'
        ]
        parser = Parser(language, tokens)
        result = parser.parse()

        assert result.accepted is True
    
    def test_parse_parenthesized_expression(self, language):
        """Test parsing expressions with parentheses."""
        tokens = [
            'program', 'abc', ';',
            'var', 'a', ',', 'b', ',', 'c', ':', 'integer', ';',
            'begin',
            'c', '=', '(', 'a', '+', 'b', ')', '*', '2', ';',
            'end'
        ]
        parser = Parser(language, tokens)
        result = parser.parse()

        assert result.accepted is True
    
    def test_parse_print_statement(self, language):
        """Test parsing print statements."""
        tokens = [
            'program', 'abc', ';',
            'var', 'a', ':', 'integer', ';',
            'begin',
            'a', '=', '5', ';',
            'print', '(', 'a', ')', ';',
            'end'
        ]
        parser = Parser(language, tokens)
        result = parser.parse()

        assert result.accepted is True
    
    def test_parse_print_with_label(self, language):
        """Test parsing print statement with label."""
        tokens = [
            'program', 'abc', ';',
            'var', 'a', ':', 'integer', ';',
            'begin',
            'a', '=', '5', ';',
            'print', '(', '"value=",', 'a', ')', ';',
            'end'
        ]
        parser = Parser(language, tokens)
        result = parser.parse()

        assert result.accepted is True
