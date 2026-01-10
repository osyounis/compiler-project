"""Abstract Syntax Tree node definitions.

This module defines the AST node classes that represent the structure
of a parsed program. Each node type corresponds to a grammar construct.

The AST (Abstract Syntax Tree) is a tree representation of the program
structure that makes it easy to traverse and generate code.
"""

from typing import List, Optional
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for all AST nodes.
    
    All nodes in the tree inherit from this class and implement
    the accept() method for the visitor pattern (used in code generation).
    """
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for code generation.
        
        This is the Visitor pattern - each node knows how to call
        the appropriate visit method on the visitor.
        
        Args:
            visitor: A code generator that visits this node.
        
        Returns:
            Whatever the visitor returns (usually generated code string).
        """
        pass


class Program(ASTNode):
    """Root node representing the entire program.
    
    Example source: 'program test; var a : integer; begin a = 5; end'
    
    Attributes:
        name: Program identifier (e.g., 'test').
        declarations: List of variable declarations.
        statements: List of statements in the program body.
    """
    
    def __init__(self, name: str, declarations: List['Declaration'], statements: List['Statement']):
        self.name = name
        self.declarations = declarations
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_program(self)


class Declaration(ASTNode):
    """Variable declaration node.
    
    Example source: 'var a, b, c : integer;'
    
    Attributes:
        names: List of variable names (e.g., ['a', 'b', 'c']).
        type_name: Type of the variables (always 'integer' in our language).
    """
    
    def __init__(self, names: List[str], type_name: str):
        self.names = names
        self.type_name = type_name
    
    def accept(self, visitor):
        return visitor.visit_declaration(self)


class Statement(ASTNode):
    """Base class for statement nodes (Assignment or PrintStatement)."""
    pass


class Assignment(Statement):
    """Assignment statement node.
    
    Example source: 'a = b + 5;'
    
    Attributes:
        variable: Name of variable being assigned to (e.g., 'a').
        expression: Expression node representing the right-hand side.
    """
    
    def __init__(self, variable: str, expression: 'Expression'):
        self.variable = variable
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


class PrintStatement(Statement):
    """Print statement node.
    
    Example source: 'print(a);' or 'print("value=", a);'
    
    Attributes:
        variable: Variable name to print (e.g., 'a').
        label: Optional label prefix (e.g., 'value=' or None).
    """
    
    def __init__(self, variable: str, label: Optional[str] = None):
        self.variable = variable
        self.label = label
    
    def accept(self, visitor):
        return visitor.visit_print(self)


class Expression(ASTNode):
    """Base class for expression nodes."""
    pass


class BinaryExpression(Expression):
    """Binary operation expression node.
    
    Example source: 'a + b' or '(x * 2) - y'
    
    Attributes:
        left: Left operand (can be another expression).
        operator: Operator string ('+', '-', '*', '/').
        right: Right operand (can be another expression).
    """
    
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


class Number(Expression):
    """Numeric literal node.
    
    Example source: '42' or '-15'
    
    Attributes:
        value: The numeric value as an integer.
    """
    
    def __init__(self, value: int):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_number(self)


class Variable(Expression):
    """Variable reference in an expression.
    
    Example source: 'a' in 'a + 5'
    
    Attributes:
        name: Variable name (e.g., 'a').
    """
    
    def __init__(self, name: str):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)
