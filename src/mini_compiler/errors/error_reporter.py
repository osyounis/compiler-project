"""Error detection and reporting for the mini compiler.

This module provides classes for collecting, categorizing, and reporting
compilation errors including lexical, syntax, and semantic errors.
"""

from enum import Enum
from typing import List, Optional, Set


class ErrorType(Enum):
    """Types of compilation errors.

    Attributes:
        LEXICAL: Errors in tokenization/lexical analysis (invalid characters, etc.)
        SYNTAX: Errors in grammar/syntax (missing semicolons, mismatched parens, etc.)
        SEMANTIC: Errors in meaning (undeclared variables, type mismatches, etc.)
    """

    LEXICAL = "Lexical Error"
    SYNTAX = "Syntax Error"
    SEMANTIC = "Semantic Error"


class CompilationError:
    """Represents a compilation error with location information.

    This class encapsulates all information about a compilation error,
    including its type, message, and location in the source code.

    Attributes:
        error_type: Category of error (LEXICAL, SYNTAX, or SEMANTIC).
        message: Human-readable description of the error.
        line: Line number where error occurred (1-indexed), or None if unknown.
        column: Column number where error occurred (1-indexed), or None if unknown.
        token: The problematic token, or None if not applicable.

    Example:
        >>> error = CompilationError(
        ...     ErrorType.SEMANTIC,
        ...     "Undeclared variable 'count'",
        ...     line=8,
        ...     token="count"
        ... )
        >>> print(error)
        Semantic Error at line 8: Undeclared variable 'count' (token: 'count')
    """

    def __init__(
        self,
        error_type: ErrorType,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        token: Optional[str] = None,
    ):
        """Initialize a compilation error.

        Args:
            error_type: Category of error.
            message: Human-readable description.
            line: Line number (1-indexed), if known.
            column: Column number (1-indexed), if known.
            token: The problematic token, if applicable.
        """
        self.error_type = error_type
        self.message = message
        self.line = line
        self.column = column
        self.token = token

    def __str__(self) -> str:
        """Format error message for display.

        Returns:
            Formatted error string with location and details.
        """
        location = ""
        if self.line is not None:
            location = f" at line {self.line}"
            if self.column is not None:
                location += f", column {self.column}"

        token_info = ""
        if self.token:
            token_info = f" (token: '{self.token}')"

        return f"{self.error_type.value}{location}: {self.message}{token_info}"


class ErrorReporter:
    """Collects and reports compilation errors.

    This class maintains a list of errors encountered during compilation
    and provides methods to report them in various formats. It supports
    detecting common semantic errors like undeclared variables.

    Attributes:
        _errors: List of compilation errors.

    Example:
        >>> reporter = ErrorReporter()
        >>> declared_vars = {'a', 'b'}
        >>> reporter.check_variable_declared('c', declared_vars, line=10)
        >>> if reporter.has_errors():
        ...     reporter.print_errors()
        Semantic Error at line 10: Undeclared variable 'c' (token: 'c')
    """

    def __init__(self):
        """Initialize an empty error reporter."""
        self._errors: List[CompilationError] = []

    def add_error(self, error: CompilationError) -> None:
        """Add an error to the report.

        Args:
            error: The compilation error to add.
        """
        self._errors.append(error)

    def has_errors(self) -> bool:
        """Check if any errors have been reported.

        Returns:
            True if there are errors, False otherwise.
        """
        return len(self._errors) > 0

    def get_errors(self) -> List[CompilationError]:
        """Return all errors.

        Returns:
            List of all compilation errors (copy of internal list).
        """
        return self._errors.copy()

    def error_count(self) -> int:
        """Return the number of errors.

        Returns:
            Total number of errors reported.
        """
        return len(self._errors)

    def clear(self) -> None:
        """Clear all errors.

        Useful for resetting the reporter between compilations.
        """
        self._errors.clear()

    def print_errors(self) -> None:
        """Print all errors to stderr.

        Prints each error on a separate line using the error's
        string representation.
        """
        import sys

        for error in self._errors:
            print(str(error), file=sys.stderr)

    def get_error_summary(self) -> str:
        """Get a summary of all errors.

        Returns:
            Multi-line string with all error messages.
        """
        return "\n".join(str(error) for error in self._errors)

    def check_variable_declared(
        self, variable: str, declared_vars: Set[str], line: Optional[int] = None
    ) -> bool:
        """Check if a variable was declared and report error if not.

        Args:
            variable: The variable name to check.
            declared_vars: Set of all declared variable names.
            line: Line number where variable is used.

        Returns:
            True if variable is declared, False if undeclared (error added).
        """
        if variable not in declared_vars:
            self.add_error(
                CompilationError(
                    ErrorType.SEMANTIC,
                    f"Undeclared variable '{variable}'",
                    line=line,
                    token=variable,
                )
            )
            return False
        return True

    def check_variable_not_redeclared(
        self, variable: str, declared_vars: Set[str], line: Optional[int] = None
    ) -> bool:
        """Check if a variable is being redeclared and report error if so.

        Args:
            variable: The variable name to check.
            declared_vars: Set of all declared variable names.
            line: Line number where variable is declared.

        Returns:
            True if variable is not already declared, False if redeclared (error added).
        """
        if variable in declared_vars:
            self.add_error(
                CompilationError(
                    ErrorType.SEMANTIC,
                    f"Variable '{variable}' already declared",
                    line=line,
                    token=variable,
                )
            )
            return False
        return True

    def add_syntax_error(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        token: Optional[str] = None,
    ) -> None:
        """Add a syntax error.

        Convenience method for adding syntax errors.

        Args:
            message: Error description.
            line: Line number.
            column: Column number.
            token: Problematic token.
        """
        self.add_error(
            CompilationError(
                ErrorType.SYNTAX, message, line=line, column=column, token=token
            )
        )

    def add_semantic_error(
        self, message: str, line: Optional[int] = None, token: Optional[str] = None
    ) -> None:
        """Add a semantic error.

        Convenience method for adding semantic errors.

        Args:
            message: Error description.
            line: Line number.
            token: Problematic token.
        """
        self.add_error(
            CompilationError(ErrorType.SEMANTIC, message, line=line, token=token)
        )
