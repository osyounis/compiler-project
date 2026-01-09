"""Mini Compiler - A predictive parser for a simple programming language.

This package implements a complete compiler pipeline from source code
to executable output in multiple target languages.
"""

__version__ = '1.0.0'
__author__ = 'Omar Younis'

from .core.language import Language
from .core.parser import Parser, ParseResult
from .core.preprocessor import Preprocessor

__all__ = [
    'Language',
    'Parser',
    'ParseResult',
    'Preprocessor',
    '__version__',
    '__author__',
]
