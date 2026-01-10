"""AST Builder for constructing Abstract Syntax Trees from token streams.

This module takes a validated token stream and builds an AST
by parsing the structure and creating appropriate node objects.
"""

from typing import List, Optional
from .ast_nodes import (
    Program, Declaration, Assignment, PrintStatement,
    BinaryExpression, Number, Variable, Expression, Statement
)


class ASTBuilder:
    """Builds an Abstract Syntax Tree from a token stream.
    
    This builder assumes tokens have already been validated by the parser.
    It walks through the token stream and constructs AST nodes based on
    the grammar structure.
    
    Example:
        >>> tokens = ['program', 'test', ';', 'var', 'a', ':', 'integer', ';',
        ...           'begin', 'a', '=', '5', ';', 'end']
        >>> builder = ASTBuilder(tokens)
        >>> ast = builder.build()
        >>> print(ast.name)  # 'test'
        >>> print(ast.declarations[0].names)  # ['a']
    """
    
    def __init__(self, tokens: List[str]):
        """Initialize builder with token stream.
        
        Args:
            tokens: List of tokens (after preprocessing, validated by parser).
        """
        self.tokens = tokens
        self.pos = 0  # Current position in token stream
    
    def build(self) -> Program:
        """Build and return the complete AST.
        
        Returns:
            Program node (root of AST).
        """
        # Expecting: program <name> ; var <decls> begin <stmts> end
        
        # Skip 'program' keyword
        self._expect('program')
        
        # Get program name
        program_name = self._current_token()
        self._advance()
        
        # Skip semicolon
        self._expect(';')
        
        # Parse declarations
        declarations = self._parse_declarations()
        
        # Skip 'begin'
        self._expect('begin')
        
        # Parse statements
        statements = self._parse_statements()
        
        # Skip 'end'
        self._expect('end')
        
        return Program(program_name, declarations, statements)
    
    def _parse_declarations(self) -> List[Declaration]:
        """Parse variable declarations.
        
        Grammar: var <id_list> : integer ;
        
        Returns:
            List of Declaration nodes.
        """
        declarations = []
        
        # Skip 'var' keyword
        self._expect('var')
        
        # Parse identifier list: a, b, c : integer ;
        var_names = []
        
        while self._current_token() != ':':
            token = self._current_token()
            if token == ',':
                self._advance()
                continue
            # Strip comma from token if it's attached (e.g., 'a,' -> 'a')
            clean_token = token.rstrip(',')
            if clean_token:  # Only add non-empty tokens
                var_names.append(clean_token)
            self._advance()
        
        # Skip ':'
        self._expect(':')
        
        # Skip type ('integer')
        type_name = self._current_token()
        self._advance()
        
        # Skip ';'
        self._expect(';')
        
        declarations.append(Declaration(var_names, type_name))
        
        return declarations
    
    def _parse_statements(self) -> List[Statement]:
        """Parse statement list.
        
        Statements are either assignments or print statements.
        
        Returns:
            List of Statement nodes.
        """
        statements = []
        
        while self._current_token() != 'end':
            token = self._current_token()
            
            if token == 'print':
                statements.append(self._parse_print())
            else:
                # Must be an assignment
                statements.append(self._parse_assignment())
        
        return statements
    
    def _parse_assignment(self) -> Assignment:
        """Parse assignment statement.
        
        Grammar: <id> = <expr> ;
        
        Returns:
            Assignment node.
        """
        # Get variable name
        var_name = self._current_token()
        self._advance()
        
        # Skip '='
        self._expect('=')
        
        # Parse expression
        expr = self._parse_expression()
        
        # Skip ';'
        self._expect(';')
        
        return Assignment(var_name, expr)
    
    def _parse_print(self) -> PrintStatement:
        """Parse print statement.
        
        Grammar: print ( [label ,] <id> ) ;
        
        Returns:
            PrintStatement node.
        """
        # Skip 'print'
        self._expect('print')
        
        # Skip '('
        self._expect('(')
        
        # Check for label
        label = None
        if '"value=",' in self.tokens[self.pos:]:
            # Has label
            label = '"value=",'
            self._expect('"value=",')
        
        # Get variable name
        var_name = self._current_token()
        self._advance()
        
        # Skip ')'
        self._expect(')')
        
        # Skip ';'
        self._expect(';')
        
        return PrintStatement(var_name, label)
    
    def _parse_expression(self) -> Expression:
        """Parse expression with operators.

        This is simplified - it handles basic precedence:
        - Multiplication/division before addition/subtraction
        - Parentheses for grouping

        Returns:
            Expression node (can be BinaryExpression, Number, or Variable).
        """
        # Collect all tokens until ';' (expressions in assignments always end with ';')
        expr_tokens = []
        while self._current_token() != ';':
            expr_tokens.append(self._current_token())
            self._advance()

        # Parse the expression tokens
        return self._build_expression_tree(expr_tokens)
    
    def _build_expression_tree(self, tokens: List[str]) -> Expression:
        """Build expression tree from token list.

        This handles operator precedence:
        1. Handle parentheses first
        2. Then addition/subtraction (lower precedence, evaluated first in scan)
        3. Then multiplication/division (higher precedence)

        Args:
            tokens: List of tokens forming an expression.

        Returns:
            Expression node.
        """
        if not tokens:
            return Number(0)

        if len(tokens) == 1:
            # Single token - could be number, variable, or already-built Expression
            token = tokens[0]
            if isinstance(token, Expression):
                return token
            elif isinstance(token, str) and token.lstrip('-').isdigit():
                return Number(int(token))
            else:
                return Variable(token)

        # Handle parentheses first
        if '(' in tokens:
            tokens = self._simplify_parentheses(tokens)
            if len(tokens) == 1:
                # After simplification, we might have a single expression
                if isinstance(tokens[0], Expression):
                    return tokens[0]

        # Find lowest precedence operator (+ or -) scanning right to left
        for i in range(len(tokens) - 1, -1, -1):
            if isinstance(tokens[i], str) and tokens[i] in ['+', '-'] and i > 0:
                left = self._build_expression_tree(tokens[:i])
                right = self._build_expression_tree(tokens[i+1:])
                return BinaryExpression(left, tokens[i], right)

        # Find higher precedence operator (* or /) scanning right to left
        for i in range(len(tokens) - 1, -1, -1):
            if isinstance(tokens[i], str) and tokens[i] in ['*', '/'] and i > 0:
                left = self._build_expression_tree(tokens[:i])
                right = self._build_expression_tree(tokens[i+1:])
                return BinaryExpression(left, tokens[i], right)

        # Shouldn't reach here, but default to first token
        if tokens[0].lstrip('-').isdigit():
            return Number(int(tokens[0]))
        return Variable(tokens[0])
    
    def _simplify_parentheses(self, tokens: List[str]) -> List[str]:
        """Simplify innermost parentheses in expression.

        Finds the innermost parenthesized expression, evaluates it,
        and replaces it in the token list.

        Args:
            tokens: Token list with parentheses.

        Returns:
            Simplified token list (may still have parentheses if nested).
        """
        # Find innermost parentheses (no nested parens inside)
        start_idx = -1
        for i in range(len(tokens)):
            if tokens[i] == '(':
                start_idx = i
            elif tokens[i] == ')' and start_idx >= 0:
                # Found matching pair
                inner_tokens = tokens[start_idx+1:i]
                inner_expr = self._build_expression_tree(inner_tokens)

                # Rebuild token list with expression replacing ( ... )
                result = tokens[:start_idx]
                result.append(inner_expr)  # Store expression object
                result.extend(tokens[i+1:])

                # Recursively simplify if more parens exist
                if '(' in result:
                    return self._simplify_parentheses(result)
                return result

        # No parentheses found
        return tokens
    
    def _current_token(self) -> str:
        """Get current token without advancing.
        
        Returns:
            Current token string.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ''
    
    def _advance(self):
        """Move to next token."""
        self.pos += 1
    
    def _expect(self, expected: str):
        """Expect a specific token and advance.
        
        Args:
            expected: The token string we expect.
        """
        if self._current_token() == expected:
            self._advance()
        # Note: We don't raise errors here because the parser already validated
