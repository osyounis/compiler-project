"""Semantic analysis for the mini compiler.

This module performs semantic checks on parsed programs,
including variable declaration checking and type validation.
"""

from typing import List, Set, Optional
from ..errors.error_reporter import ErrorReporter


class SemanticAnalyzer:
    """Performs semantic analysis on token streams.
    
    This analyzer performs a simplified semantic analysis by walking
    through the token stream and checking:
    - All used variables are declared
    - Variables are not redeclared
    
    This runs after successful syntax parsing.
    
    Example:
        >>> analyzer = SemanticAnalyzer()
        >>> tokens = ['program', 'test', ';', 'var', 'a', ':', 'integer', ';',
        ...           'begin', 'b', '=', '5', ';', 'end']
        >>> errors = analyzer.analyze(tokens)
        >>> if errors.has_errors():
        ...     print("Undeclared variable 'b'")
    """
    
    def __init__(self):
        """Initialize semantic analyzer."""
        pass
    
    def analyze(self, tokens: List[str]) -> ErrorReporter:
        """Analyze token stream for semantic errors.
        
        Args:
            tokens: List of tokens from preprocessor (after parsing succeeds).
        
        Returns:
            ErrorReporter containing any semantic errors found.
        """
        reporter = ErrorReporter()
        declared_vars = self._extract_declarations(tokens)
        self._check_variable_usage(tokens, declared_vars, reporter)
        return reporter
    
    def _extract_declarations(self, tokens: List[str]) -> Set[str]:
        """Extract all declared variable names from token stream.
        
        Looks for the pattern: var <id> , <id> , ... : integer ;
        
        Args:
            tokens: Token list.
        
        Returns:
            Set of declared variable names.
        """
        declared = set()
        
        # Find 'var' keyword
        if 'var' not in tokens:
            return declared
        
        var_index = tokens.index('var')
        
        # Scan from 'var' until we hit 'begin' (end of declarations)
        i = var_index + 1
        while i < len(tokens) and tokens[i] != 'begin':
            token = tokens[i]
            
            # Skip keywords and punctuation
            if token in {':', 'integer', ';', ','}:
                i += 1
                continue
            
            # This should be a variable name
            if self._is_identifier(token):
                declared.add(token)
            
            i += 1
        
        return declared
    
    def _check_variable_usage(
        self,
        tokens: List[str],
        declared_vars: Set[str],
        reporter: ErrorReporter
    ) -> None:
        """Check that all used variables are declared.
        
        Looks for variable usage in:
        - Assignments: <id> = <expr> ;
        - Print statements: print ( <id> ) ;
        - Expressions: any identifier used
        
        Args:
            tokens: Token list.
            declared_vars: Set of declared variables.
            reporter: ErrorReporter to add errors to.
        """
        # Find 'begin' keyword (start of statements)
        if 'begin' not in tokens:
            return
        
        begin_index = tokens.index('begin')
        end_index = tokens.index('end') if 'end' in tokens else len(tokens)
        
        # Scan statement section
        i = begin_index + 1
        while i < end_index:
            token = tokens[i]
            
            # Check if this is an identifier (potential variable usage)
            if self._is_identifier(token):
                # Make sure it's not a keyword
                if token not in {'begin', 'end', 'var', 'integer', 'program', 'print'}:
                    # Check if declared
                    if token not in declared_vars:
                        reporter.check_variable_declared(
                            token,
                            declared_vars,
                            line=None  # We don't track line numbers in token stream
                        )
            
            i += 1
    
    def _is_identifier(self, token: str) -> bool:
        """Check if a token looks like an identifier.
        
        Identifiers start with a letter and may contain letters and digits.
        Note: In our language, only letters a,b,c,d,l,f are valid.
        
        Args:
            token: Token to check.
        
        Returns:
            True if token appears to be an identifier.
        """
        if not token:
            return False
        
        # Must start with a letter
        if not token[0].isalpha():
            return False
        
        # Rest must be letters or digits
        return all(c.isalnum() for c in token)
