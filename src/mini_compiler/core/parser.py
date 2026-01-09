"""Predictive parser implementation using LL(1) parsing.

This module contains the Parser class which performs syntax analysis
using table-driven predictive parsing with an explicit stack.
"""

from typing import List, Optional, Set
from .language import Language
from ..utils.constants import EPSILON, END_MARKER


class ParseResult:
    """Result of a parsing operation.

    Attributes:
        accepted: Whether the input was syntactically valid.
        error_message: Description of error if rejected, None if accepted.
        position: Token position where error occurred, if applicable.
    """

    def __init__(
        self, 
        accepted: bool, 
        error_message: Optional[str] = None,
        position: Optional[int] = None
    ):
        """Initialize parse result.

        Args:
            accepted: True if parsing succeeded, False otherwise.
            error_message: Error description if parsing failed.
            position: Token index where error occurred.
        """
        self.accepted = accepted
        self.error_message = error_message
        self.position = position


class Parser:
    """Predictive parser using table-driven LL(1) parsing algorithm.

    This parser validates whether an input token stream conforms to
    the language grammar. It uses a stack-based approach with a parsing
    table to guide derivations, implementing the standard LL(1) parsing
    algorithm.

    The parsing process:
    1. Initialize stack with end marker ($) and start symbol
    2. For each input token:
       a. Pop top of stack
       b. If it matches token, advance to next token
       c. If it's a non-terminal, look up production in table
       d. Push production symbols onto stack in reverse order
    3. Accept if stack empties correctly, reject on table lookup failure

    Attributes:
        _language: The language grammar specification.
        _tokens: List of input tokens to parse.

    Example:
        >>> from mini_compiler.core.language import Language
        >>> from mini_compiler.utils.constants import (
        ...     PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS
        ... )
        >>> language = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
        >>> tokens = ['program', 'test', ';', 'var', 'a', ':', 'integer', ';',
        ...           'begin', 'a', '=', '5', ';', 'print', '(', 'a', ')', ';', 'end']
        >>> parser = Parser(language, tokens)
        >>> result = parser.parse()
        >>> if result.accepted:
        ...     print("Valid program!")
        Valid program!
    """

    def __init__(self, language: Language, tokens: List[str]) -> None:
        """Initialize parser with language and token stream.

        Args:
            language: The Language object containing grammar rules and parsing table.
            tokens: List of tokens from preprocessor to parse.
        """
        self._language = language
        self._tokens = tokens

    def parse(self) -> ParseResult:
        """Execute predictive parsing algorithm.

        Implements the standard LL(1) table-driven parsing algorithm
        with error detection and position tracking.

        Returns:
            ParseResult indicating success/failure and any error details.
        """
        if not self._tokens:
            return ParseResult(
                False,
                "Empty input - expected a program",
                0
            )

        # Initialize stack with end marker and start symbol
        stack = [END_MARKER, self._language.get_starting_state()]
        token_index = 0
        valid_symbols = set(self._language.get_indexes().keys())

        while token_index < len(self._tokens):
            token = self._tokens[token_index]

            # Handle multi-character tokens not in symbol table
            # (identifiers and numbers longer than 1 char)
            if token not in valid_symbols:
                success, new_index = self._process_multichar_token(
                    token, stack, token_index, valid_symbols
                )
                if not success:
                    return ParseResult(
                        False,
                        f"Syntax error at token '{token}' (position {token_index})",
                        token_index
                    )
                token_index = new_index
                continue

            # Process single-character token or keyword
            if not stack:
                return ParseResult(
                    False,
                    f"Unexpected token '{token}' (position {token_index}) - input too long",
                    token_index
                )

            control_char = stack.pop()

            # Match: terminal on stack matches input token
            if token == control_char:
                token_index += 1
                continue

            # Lookup production in parsing table
            production = self._language.get_control_chars(control_char, token)

            if production == '':
                # No valid production - syntax error
                return ParseResult(
                    False,
                    f"Unexpected token '{token}' at position {token_index} "
                    f"(expected something else for {control_char})",
                    token_index
                )
            elif production == EPSILON:
                # Epsilon production - continue without consuming token
                continue
            else:
                # Push production symbols onto stack in reverse order
                for symbol in reversed(production.split()):
                    stack.append(symbol)

        # Check if stack is properly emptied (only $ remains)
        if stack and stack.pop() == END_MARKER:
            return ParseResult(True)
        else:
            return ParseResult(
                False,
                "Unexpected end of input (incomplete program)",
                token_index
            )

    def _process_multichar_token(
        self,
        token: str,
        stack: List[str],
        position: int,
        valid_symbols: Set[str]
    ) -> tuple[bool, int]:
        """Process multi-character token character by character.

        Handles identifiers and numbers that don't appear as single
        entries in the symbol table. Processes each character against
        the parsing table.

        Args:
            token: The multi-character token to process.
            stack: The parsing stack (modified in place).
            position: Current position in token stream.
            valid_symbols: Set of valid grammar symbols.

        Returns:
            Tuple of (success: bool, next_position: int).
            success is True if token processed successfully.
            next_position is position + 1 if successful.
        """
        char_index = 0
        while char_index < len(token):
            char = token[char_index]

            if not stack:
                return False, position

            control_char = stack.pop()

            # Match: character matches stack top
            if char == control_char:
                char_index += 1
                continue

            # Lookup production for this character
            production = self._language.get_control_chars(control_char, char)

            if production == '':
                # No valid production - error
                return False, position
            elif production == EPSILON:
                # Epsilon production - continue without advancing char_index
                continue
            else:
                # Push production symbols onto stack in reverse
                for symbol in reversed(production.split()):
                    stack.append(symbol)

        return True, position + 1


# Legacy compatibility classes - marked for deprecation
class Trace:
    """Deprecated: Use Parser class instead.

    This class is maintained for backward compatibility with the original
    implementation but will be removed in a future version. Use Parser directly.
    """

    def __init__(self, user_input: 'InputStatement', language: Language) -> None:
        """Initialize Trace with legacy InputStatement interface."""
        tokens = user_input.get_statement()
        parser = Parser(language, tokens)
        result = parser.parse()
        user_input.set_accepted(result.accepted)
        self._print_result(result)

    def _print_result(self, result: ParseResult) -> None:
        """Print parsing result in legacy format."""
        if result.accepted:
            print("Ready to compile.")
        else:
            print(f"ERROR: Cannot compile. {result.error_message or ''}")


class InputStatement:
    """Deprecated: Use Preprocessor directly.

    This class is maintained for backward compatibility but will be removed
    in a future version. Use the Preprocessor class for tokenization.
    """

    def __init__(self, filename: str) -> None:
        """Initialize InputStatement by reading and tokenizing a file."""
        self._accepted = None

        with open(filename, 'r', encoding='utf-8') as f_obj:
            lines = f_obj.readlines()
        content = [line.strip().split() for line in lines]

        # Flatten into single list of tokens
        content_list = []
        for line in content:
            for character in line:
                content_list.append(character)

        self._contents = content_list

    def set_accepted(self, flag: bool) -> None:
        """Set acceptance flag."""
        self._accepted = flag

    def get_accepted(self) -> bool:
        """Get acceptance flag."""
        return self._accepted

    def get_statement(self) -> List[str]:
        """Get token list."""
        return self._contents
