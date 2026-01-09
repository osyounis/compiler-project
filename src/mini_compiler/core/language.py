"""Language definition and grammar rules for the mini compiler.

This module contains the Language class which encapsulates the formal grammar
specification and predictive parsing table for the simple programming language.
"""

from typing import Dict, List, Set, Optional


class Language:
    """Represents a formal language with predictive parsing table.
    
    This class encapsulates the grammar rules and parsing table for the
    simple programming language. It provides methods to query the parsing
    table during predictive parsing using an LL(1) parsing algorithm.
    
    The language grammar includes:
    - Variable declarations (integer type only)
    - Assignment statements with arithmetic expressions
    - Print statements with optional labels
    - Comments (removed during preprocessing)
    
    Attributes:
        _starting_state: The start symbol of the grammar (e.g., 'Program').
        _parsing_table: 2D table mapping (non-terminal, terminal) to productions.
        _indexes: Maps grammar symbols to row/column indices in parsing table.
        _reserved_words: Set of keywords that cannot be used as identifiers.
    
    Example:
        >>> from mini_compiler.utils.constants import (
        ...     PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS
        ... )
        >>> lang = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
        >>> production = lang.get_control_chars('Expression', '+')
        >>> print(production)  # Returns the production to apply
        '+ Term ExpressionTail'
    """
    
    def __init__(self,
                 starting_state: str,
                 parsing_table: List[List[Optional[str]]],
                 indexes: Dict[str, int],
                 reserved: Set[str]) -> None:
        """Initialize the Language with grammar specification.
        
        Args:
            starting_state: The start symbol of the grammar (e.g., 'Program').
            parsing_table: The predictive parsing table as a 2D list.
                Each cell contains either:
                - A production rule string (e.g., 'Term ExpressionTail')
                - 'lambda' for epsilon (ε) productions
                - Empty string '' for error/no valid production
            indexes: Mapping of symbols (terminals and non-terminals) to
                table indices. Terminals map to column indices,
                non-terminals map to row indices.
            reserved: Set of reserved keywords that cannot be used as
                user-defined identifiers.
        
        Raises:
            KeyError: If starting_state is not in indexes.
        """
        self._starting_state = starting_state
        self._parsing_table = parsing_table
        self._indexes = indexes
        self._reserved_words = reserved

    def get_indexes(self) -> Dict[str, int]:
        """Return the symbol-to-index mapping.
        
        Returns:
            Dictionary mapping grammar symbols to their indices in the
            parsing table. Terminals map to column indices, non-terminals
            map to row indices.
        """
        return self._indexes

    def get_control_chars(self, non_terminal: str, terminal: str) -> Optional[str]:
        """Retrieve production from parsing table.
        
        Given a non-terminal on the stack and a terminal from input,
        returns the production to apply according to the LL(1) parsing
        table. This is the core lookup operation for table-driven parsing.
        
        Args:
            non_terminal: The non-terminal symbol from stack top.
                Must be a valid non-terminal in the grammar.
            terminal: The current terminal from input stream.
                Must be a valid terminal in the grammar.
        
        Returns:
            Production string to push onto stack (space-separated symbols),
            'lambda' for epsilon (ε) productions (pop without pushing),
            or empty string '' if no valid production (syntax error).
        
        Example:
            >>> lang.get_control_chars('Expression', 'a')
            'Term ExpressionTail'
            >>> lang.get_control_chars('ExpressionTail', ';')
            'lambda'
            >>> lang.get_control_chars('Expression', ')')
            ''
        """
        non_terminal_index = self._indexes[non_terminal]
        terminal_index = self._indexes[terminal]
        return self._parsing_table[non_terminal_index][terminal_index]

    def get_starting_state(self) -> str:
        """Return the grammar's start symbol.
        
        Returns:
            The start symbol (root non-terminal) of the grammar,
            typically 'Program'.
        """
        return self._starting_state

    def is_reserved_word(self, word: str) -> bool:
        """Check if a word is a reserved keyword.
        
        Args:
            word: The word to check.
        
        Returns:
            True if word is a reserved keyword, False otherwise.
        """
        return word in self._reserved_words

    def get_reserved_words(self) -> Set[str]:
        """Return the set of reserved keywords.
        
        Returns:
            Set of all reserved keywords in the language.
        """
        return self._reserved_words.copy()
