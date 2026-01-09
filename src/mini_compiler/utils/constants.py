"""Constants and configurations for the mini compiler.

This module contains all the constants used throughout the compiler,
including the grammar symbol mappings, parsing table, and reserved words.
"""

from typing import Dict, List, Set, Optional

# Special parsing symbols
EPSILON: str = 'lambda'  # Represents epsilon (ε) production
END_MARKER: str = '$'    # Marks end of input

# Reserved keywords in the language
RESERVED_WORDS: Set[str] = {
    'program', 'begin', 'end', 'var', 'integer', 'print'
}

# Terminal symbols in the language grammar
TERMINAL_SYMBOLS: Set[str] = {
    'a', 'b', 'c', 'd', 'l', 'f',  # Letters (limited alphabet)
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  # Digits
    '+', '-', '*', '/',  # Arithmetic operators
    ';', ':', '(', ')', ',', '=',  # Punctuation and delimiters
    '"value=",',  # String literal
    'print', 'integer', 'program', 'begin', 'end', 'var', '$'  # Keywords + end marker
}

# Symbol table indices - maps grammar symbols to parsing table row/column indices
# Terminals (0-32): column indices in parsing table
# Non-terminals: row indices in parsing table
SYMBOL_INDICES: Dict[str, int] = {
    # Terminals - column indices (0-32)
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'l': 4,
    'f': 5,
    '0': 6,
    '1': 7,
    '2': 8,
    '3': 9,
    '4': 10,
    '5': 11,
    '6': 12,
    '7': 13,
    '8': 14,
    '9': 15,
    '+': 16,
    '-': 17,
    '*': 18,
    '/': 19,
    ';': 20,
    ':': 21,
    '(': 22,
    ')': 23,
    ',': 24,
    '=': 25,
    '"value=",': 26,
    'print': 27,
    'integer': 28,
    'program': 29,
    'begin': 30,
    'end': 31,
    '$': 32,
    'var': 32,
    
    # Non-terminals - row indices (0-22)
    'Program': 0,
    'Identifier': 1,
    'IdentifierRest': 2,
    'DeclarationBlock': 3,
    'IdentifierList': 4,
    'IdentifierListTail': 5,
    'Type': 6,
    'StatementList': 7,
    'StatementListTail': 8,
    'Statement': 9,
    'PrintStatement': 10,
    'PrintPrefix': 11,
    'Assignment': 12,
    'Expression': 13,
    'ExpressionTail': 14,
    'Term': 15,
    'TermTail': 16,
    'Factor': 17,
    'Number': 18,
    'NumberTail': 19,
    'Sign': 20,
    'Digit': 21,
    'Letter': 22,
}

# Predictive Parsing Table
# 23 rows (non-terminals) x 33 columns (terminals)
# Each cell contains: production rule string, 'lambda' for ε-production, or '' for error
PARSING_TABLE: List[List[Optional[str]]] = [
    # Row 0: Program
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'program Identifier ; var DeclarationBlock begin StatementList end', '', '', '', ''],
    
    # Row 1: Identifier
    ['Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 2: IdentifierRest
    ['Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Letter IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'Digit IdentifierRest', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', 'lambda', 'lambda', 'lambda', '', '', '', '', '', '', '', ''],
    
    # Row 3: DeclarationBlock
    ['IdentifierList : Type ;', 'IdentifierList : Type ;', 'IdentifierList : Type ;', 'IdentifierList : Type ;', 'IdentifierList : Type ;', 'IdentifierList : Type ;', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 4: IdentifierList
    ['Identifier IdentifierListTail', 'Identifier IdentifierListTail', 'Identifier IdentifierListTail', 'Identifier IdentifierListTail', 'Identifier IdentifierListTail', 'Identifier IdentifierListTail', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 5: IdentifierListTail
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'lambda', '', '', ', IdentifierList', '', '', '', '', '', '', '', '', ''],
    
    # Row 6: Type
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'integer', '', '', '', '', ''],
    
    # Row 7: StatementList
    ['Statement StatementListTail', 'Statement StatementListTail', 'Statement StatementListTail', 'Statement StatementListTail', 'Statement StatementListTail', 'Statement StatementListTail', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Statement StatementListTail', '', '', '', 'lambda', '', ''],
    
    # Row 8: StatementListTail
    ['StatementList', 'StatementList', 'StatementList', 'StatementList', 'StatementList', 'StatementList', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'StatementList', '', '', '', 'lambda', '', ''],
    
    # Row 9: Statement
    ['Assignment', 'Assignment', 'Assignment', 'Assignment', 'Assignment', 'Assignment', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'PrintStatement', '', '', '', '', '', ''],
    
    # Row 10: PrintStatement
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'print ( PrintPrefix Identifier ) ;', '', '', '', '', '', ''],
    
    # Row 11: PrintPrefix
    ['lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '"value=",', '', '', '', '', '', '', ''],
    
    # Row 12: Assignment
    ['Identifier = Expression ;', 'Identifier = Expression ;', 'Identifier = Expression ;', 'Identifier = Expression ;', 'Identifier = Expression ;', 'Identifier = Expression ;', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 13: Expression
    ['Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', 'Term ExpressionTail', '', '', '', '', 'Term ExpressionTail', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 14: ExpressionTail
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '+ Term ExpressionTail', '- Term ExpressionTail', '', '', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 15: Term
    ['Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', 'Factor TermTail', '', '', '', '', 'Factor TermTail', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 16: TermTail
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'lambda', 'lambda', '* Factor TermTail', '/ Factor TermTail', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '',''],
    
    # Row 17: Factor
    ['Identifier', 'Identifier', 'Identifier', 'Identifier', 'Identifier', 'Identifier', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', '', '', '', '', '( Expression )', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 18: Number
    ['', '', '', '', '', '', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', 'Sign Digit NumberTail', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 19: NumberTail
    ['', '', '', '', '', '', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'Digit NumberTail', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 20: Sign
    ['', '', '', '', '', '', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '+', '-', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 21: Digit
    ['', '', '', '', '', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    # Row 22: Letter
    ['a', 'b', 'c', 'd', 'l', 'f', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'print ( PrintPrefix Identifier ) ;', '', '', '', '', '', '']
]
