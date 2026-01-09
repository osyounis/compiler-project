"""Command-line interface for the mini compiler.

This module provides the CLI entry point for the mini compiler,
supporting both validation and compilation commands.
"""

import argparse
import sys
from pathlib import Path

from .core.language import Language
from .core.parser import Parser
from .core.preprocessor import Preprocessor
from .utils.constants import (
    PARSING_TABLE,
    SYMBOL_INDICES,
    RESERVED_WORDS,
)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog='mini-compiler',
        description='Mini Compiler - Compile simple programs to multiple languages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate syntax only
  python -m mini_compiler validate examples/valid/example1.src
  
  # Compile to Python
  python -m mini_compiler compile examples/valid/example1.src --output python -o output.py
  
  # Compile to C++ with verbose mode
  python -m mini_compiler compile examples/valid/example1.src --output cpp -o output.cpp -v
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate source code syntax without generating code'
    )
    validate_parser.add_argument(
        'input',
        type=str,
        help='Path to source file (.src)'
    )
    validate_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed parsing information (token list, etc.)'
    )
    
    # Compile command
    compile_parser = subparsers.add_parser(
        'compile',
        help='Compile source code to target language'
    )
    compile_parser.add_argument(
        'input',
        type=str,
        help='Path to source file (.src)'
    )
    compile_parser.add_argument(
        '--output',
        type=str,
        choices=['python', 'cpp', 'java', 'csharp'],
        default='python',
        help='Target language for code generation (default: python)'
    )
    compile_parser.add_argument(
        '-o', '--outfile',
        type=str,
        help='Output file path (default: stdout)'
    )
    compile_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed compilation information'
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize compiler components
    language = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
    preprocessor = Preprocessor()
    
    try:
        # Preprocess source file
        if args.verbose:
            print(f"Preprocessing {args.input}...", file=sys.stderr)
        
        tokens = preprocessor.process_file(str(input_path))
        
        if args.verbose:
            print(f"Tokens ({len(tokens)}): {' '.join(tokens[:20])}{'...' if len(tokens) > 20 else ''}", 
                  file=sys.stderr)
        
        # Parse tokens
        if args.verbose:
            print("Parsing...", file=sys.stderr)
        
        parser_obj = Parser(language, tokens)
        result = parser_obj.parse()
        
        # Handle validate command
        if args.command == 'validate':
            if result.accepted:
                print("✓ Syntax valid - ready to compile")
                sys.exit(0)
            else:
                print(f"✗ Syntax error: {result.error_message}", file=sys.stderr)
                sys.exit(1)
        
        # Handle compile command
        elif args.command == 'compile':
            if not result.accepted:
                print(f"✗ Compilation failed: {result.error_message}", file=sys.stderr)
                sys.exit(1)
            
            if args.verbose:
                print(f"Generating {args.output} code...", file=sys.stderr)
            
            # TODO: Code generation will be implemented in Phase 4
            print("✗ Code generation not yet implemented", file=sys.stderr)
            print("   This feature will be added in Phase 4 of the refactoring.", file=sys.stderr)
            sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
