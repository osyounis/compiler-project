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
from .utils.constants import PARSING_TABLE, RESERVED_WORDS, SYMBOL_INDICES


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="mini-compiler",
        description="Mini Compiler - Compile simple programs to multiple languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate syntax only
  python -m mini_compiler validate examples/valid/example1.src
  
  # Compile to Python
  python -m mini_compiler compile examples/valid/example1.src --output python -o output.py
  
  # Compile to C++ with verbose mode
  python -m mini_compiler compile examples/valid/example1.src --output cpp -o output.cpp -v
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate source code syntax without generating code"
    )
    validate_parser.add_argument("input", type=str, help="Path to source file (.src)")
    validate_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed parsing information (token list, etc.)",
    )

    # Compile command
    compile_parser = subparsers.add_parser(
        "compile", help="Compile source code to target language"
    )
    compile_parser.add_argument("input", type=str, help="Path to source file (.src)")
    compile_parser.add_argument(
        "--output",
        type=str,
        choices=["python", "cpp", "java", "csharp"],
        default="python",
        help="Target language for code generation (default: python)",
    )
    compile_parser.add_argument(
        "-o", "--outfile", type=str, help="Output file path (default: stdout)"
    )
    compile_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed compilation information",
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
    language = Language("Program", PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
    preprocessor = Preprocessor()

    try:
        # Preprocess source file
        if args.verbose:
            print(f"Preprocessing {args.input}...", file=sys.stderr)

        tokens = preprocessor.process_file(str(input_path))

        if args.verbose:
            print(
                f"Tokens ({len(tokens)}): {' '.join(tokens[:20])}{'...' if len(tokens) > 20 else ''}",
                file=sys.stderr,
            )

        # Parse tokens (with semantic analysis for validate command)
        if args.verbose:
            print("Parsing...", file=sys.stderr)

        parser_obj = Parser(language, tokens)

        # Handle validate command
        if args.command == "validate":
            result = parser_obj.parse_with_semantics()

            if not result.accepted:
                print(f"✗ Syntax error: {result.error_message}", file=sys.stderr)
                sys.exit(1)

            # Check for semantic errors
            if result.semantic_errors.has_errors():
                print(
                    f"✗ Semantic errors found ({result.semantic_errors.error_count()}):",
                    file=sys.stderr,
                )
                result.semantic_errors.print_errors()
                sys.exit(1)

            print("✓ Program is valid - ready to compile")
            sys.exit(0)

        # Handle compile command
        elif args.command == "compile":
            # Parse and build AST
            result = parser_obj.parse_with_ast()

            if not result.accepted:
                print(f"✗ Compilation failed: {result.error_message}", file=sys.stderr)
                sys.exit(1)

            if not result.ast:
                print("✗ Failed to build AST", file=sys.stderr)
                sys.exit(1)

            if args.verbose:
                print(f"Generating {args.output} code...", file=sys.stderr)

            # Select code generator based on output language
            if args.output == "python":
                from .codegen.python_gen import PythonGenerator

                generator = PythonGenerator()
            elif args.output == "cpp":
                print("✗ C++ code generation not yet implemented", file=sys.stderr)
                print("   Currently only Python is supported.", file=sys.stderr)
                sys.exit(1)
            elif args.output == "java":
                print("✗ Java code generation not yet implemented", file=sys.stderr)
                print("   Currently only Python is supported.", file=sys.stderr)
                sys.exit(1)
            elif args.output == "csharp":
                print("✗ C# code generation not yet implemented", file=sys.stderr)
                print("   Currently only Python is supported.", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"✗ Unknown output language: {args.output}", file=sys.stderr)
                sys.exit(1)

            # Generate code
            try:
                generated_code = generator.generate(result.ast)

                # Output to file or stdout
                if args.outfile:
                    with open(args.outfile, "w", encoding="utf-8") as f:
                        f.write(generated_code)
                    print(f"✓ Generated {args.output} code → {args.outfile}")
                else:
                    # Print to stdout
                    print(generated_code)

                sys.exit(0)

            except Exception as e:
                print(f"✗ Code generation failed: {e}", file=sys.stderr)
                if args.verbose:
                    import traceback

                    traceback.print_exc()
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


if __name__ == "__main__":
    main()
