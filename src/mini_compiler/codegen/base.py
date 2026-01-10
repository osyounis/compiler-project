"""Abstract base class for code generators.

This module defines the CodeGenerator base class that all language-specific
generators inherit from. It uses the Visitor pattern to traverse the AST
and generate code.
"""

from abc import ABC, abstractmethod
from typing import List


class CodeGenerator(ABC):
    """Base class for all code generators using Visitor pattern.
    
    Each language-specific generator (Python, C++, Java, C#) inherits
    from this class and implements the visit_* methods to output code
    in that language's syntax.
    
    The Visitor pattern works like this:
    1. AST node calls: visitor.visit_program(self)
    2. Visitor generates code for that node type
    3. Node's children call visitor recursively
    4. Result: Complete program in target language!
    
    Attributes:
        _output: List of output lines (strings).
        _indent_level: Current indentation level (for formatting).
    
    Example:
        class MyGenerator(CodeGenerator):
            def visit_program(self, node):
                self._emit(f"// Program: {node.name}")
                for stmt in node.statements:
                    stmt.accept(self)
    """
    
    def __init__(self):
        """Initialize code generator."""
        self._output: List[str] = []
        self._indent_level = 0
    
    def generate(self, ast_root) -> str:
        """Generate code from AST root node.
        
        This is the main entry point. It visits the root node
        (Program) which recursively visits all children, building
        up the output.
        
        Args:
            ast_root: The Program node (root of AST).
        
        Returns:
            Complete generated code as a string.
        """
        self._output.clear()
        self._indent_level = 0
        ast_root.accept(self)  # Start visiting from root
        return '\n'.join(self._output)
    
    def _emit(self, line: str) -> None:
        """Emit a line of code with current indentation.
        
        Args:
            line: Line of code to output (without indentation).
        """
        indent = '    ' * self._indent_level  # 4 spaces per level
        self._output.append(indent + line)
    
    def _emit_blank(self) -> None:
        """Emit a blank line (for readability)."""
        self._output.append('')
    
    def _indent(self) -> None:
        """Increase indentation level."""
        self._indent_level += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level."""
        if self._indent_level > 0:
            self._indent_level -= 1
    
    # Abstract methods - each generator must implement these
    
    @abstractmethod
    def visit_program(self, node):
        """Visit Program node.
        
        Args:
            node: Program AST node.
        """
        pass
    
    @abstractmethod
    def visit_declaration(self, node):
        """Visit Declaration node.
        
        Args:
            node: Declaration AST node.
        """
        pass
    
    @abstractmethod
    def visit_assignment(self, node):
        """Visit Assignment node.
        
        Args:
            node: Assignment AST node.
        """
        pass
    
    @abstractmethod
    def visit_print(self, node):
        """Visit PrintStatement node.
        
        Args:
            node: PrintStatement AST node.
        """
        pass
    
    @abstractmethod
    def visit_binary_expression(self, node):
        """Visit BinaryExpression node.
        
        Args:
            node: BinaryExpression AST node.
        
        Returns:
            String representation of the expression.
        """
        pass
    
    @abstractmethod
    def visit_number(self, node):
        """Visit Number node.
        
        Args:
            node: Number AST node.
        
        Returns:
            String representation of the number.
        """
        pass
    
    @abstractmethod
    def visit_variable(self, node):
        """Visit Variable node.
        
        Args:
            node: Variable AST node.
        
        Returns:
            String representation of the variable.
        """
        pass
