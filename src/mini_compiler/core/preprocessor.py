"""Preprocessor for removing comments and normalizing source code.

This module handles the lexical preprocessing phase of compilation,
including comment removal, whitespace normalization, and tokenization.
"""

import re
from typing import List
from pathlib import Path


class Preprocessor:
    """Handles preprocessing of source files before parsing.

    The preprocessor performs the following operations:
    1. Removes (* ... *) style comments
    2. Normalizes whitespace (multiple spaces → single space)
    3. Removes blank lines
    4. Tokenizes input into a list of tokens

    This corresponds to the lexical analysis phase of compilation.

    Example:
        >>> preprocessor = Preprocessor()
        >>> tokens = preprocessor.process_file('program.src')
        >>> print(tokens)
        ['program', 'test', ';', 'var', 'a', ':', 'integer', ...]

        >>> source = "program test; (* comment *) var a : integer ;"
        >>> tokens = preprocessor.process_string(source)
        >>> print(tokens)
        ['program', 'test', ';', 'var', 'a', ':', 'integer', ';']
    """

    # Regex pattern to match (* ... *) comments (including multiline)
    COMMENT_PATTERN = re.compile(r'\(\*.*?\*\)', re.DOTALL)

    # Regex pattern to match one or more whitespace characters
    WHITESPACE_PATTERN = re.compile(r'\s+')

    def process_file(self, filepath: str) -> List[str]:
        """Process source file and return token list.

        Reads the source file, removes comments, normalizes whitespace,
        and tokenizes the content into a list of strings. All tokens are
        converted to lowercase for case-insensitive parsing.

        Args:
            filepath: Path to the source file to process.

        Returns:
            List of tokens (strings, all lowercase) extracted from the file.

        Raises:
            FileNotFoundError: If the source file doesn't exist.
            IOError: If the file cannot be read.
            PermissionError: If there are insufficient permissions to read the file.

        Example:
            >>> preprocessor = Preprocessor()
            >>> tokens = preprocessor.process_file('examples/valid/example1.src')
            >>> # 'Program ABC;' becomes ['program', 'abc;']
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Source file not found: {filepath}")
        except PermissionError:
            raise PermissionError(f"Permission denied reading file: {filepath}")
        except IOError as e:
            raise IOError(f"Error reading file {filepath}: {e}")

        return self._process_content(content)

    def process_string(self, source: str) -> List[str]:
        """Process source code from string and return token list.

        Useful for testing and REPL-style interfaces where source code
        is provided as a string rather than from a file. All tokens are
        converted to lowercase for case-insensitive parsing.

        Args:
            source: Source code string to process.

        Returns:
            List of tokens (strings, all lowercase) extracted from the source.

        Example:
            >>> preprocessor = Preprocessor()
            >>> source = "Program ABC; Var A : Integer ;"
            >>> tokens = preprocessor.process_string(source)
            >>> print(tokens)
            ['program', 'abc;', 'var', 'a', ':', 'integer', ';']
        """
        return self._process_content(source)

    def _process_content(self, content: str) -> List[str]:
        """Internal method to process content string.

        Performs comment removal, whitespace normalization, and tokenization.
        All tokens are converted to lowercase for case-insensitive parsing.

        Args:
            content: Raw source code content.

        Returns:
            List of tokens (all lowercase).
        """
        # Remove all (* ... *) style comments
        content = self.COMMENT_PATTERN.sub('', content)

        # Process line by line, normalizing whitespace and removing blank lines
        tokens = []
        for line in content.splitlines():
            line = line.strip()
            if line:  # Skip empty lines
                # Normalize multiple spaces to single space
                normalized = self.WHITESPACE_PATTERN.sub(' ', line)
                # Split into tokens and convert to lowercase for case-insensitive parsing
                tokens.extend(token.lower() for token in normalized.split())

        return tokens

    def save_preprocessed(self, filepath: str, output_path: str) -> None:
        """Process a file and save the preprocessed output.

        This is useful for debugging or when you want to see the
        preprocessed output before parsing.

        Args:
            filepath: Path to source file to process.
            output_path: Path where preprocessed output should be saved.

        Raises:
            FileNotFoundError: If source file doesn't exist.
            IOError: If files cannot be read or written.
        """
        tokens = self.process_file(filepath)

        # Reconstruct text from tokens (space-separated)
        preprocessed_content = ' '.join(tokens)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(preprocessed_content)
        except IOError as e:
            raise IOError(f"Error writing to file {output_path}: {e}")
