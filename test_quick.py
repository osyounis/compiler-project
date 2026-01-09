#!/usr/bin/env python3
"""Quick test script to verify the compiler works."""

import sys
sys.path.insert(0, 'src')

from mini_compiler import Language, Parser, Preprocessor
from mini_compiler.utils.constants import PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS

def test_preprocessor():
    """Test the preprocessor."""
    print("Testing Preprocessor...")
    preprocessor = Preprocessor()

    # Test with example1.src
    tokens = preprocessor.process_file('examples/valid/example1.src')
    print(f"  ✓ Loaded {len(tokens)} tokens from example1.src")
    print(f"  First 10 tokens: {tokens[:10]}")

    # Test with string (note: language only supports letters a,b,c,d,l,f)
    source = "program abc; (* comment *) var a : integer ;"
    tokens = preprocessor.process_string(source)
    print(f"  ✓ Processed string: {tokens}")

    # Test case-insensitive tokenization
    source_upper = "Program ABC; Var A : Integer ;"
    tokens_upper = preprocessor.process_string(source_upper)
    print(f"  ✓ Uppercase input: {tokens_upper}")
    print(f"  Note: All tokens converted to lowercase (case-insensitive)")
    print(f"  Note: Language has limited alphabet (a,b,c,d,l,f only)")
    print()

def test_parser_valid():
    """Test parser with valid input."""
    print("Testing Parser with valid input...")
    preprocessor = Preprocessor()
    language = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
    
    # Test with example1.src
    tokens = preprocessor.process_file('examples/valid/example1.src')
    parser = Parser(language, tokens)
    result = parser.parse()
    
    if result.accepted:
        print("  ✓ example1.src parsed successfully!")
    else:
        print(f"  ✗ FAILED: {result.error_message}")
    print()

def test_parser_invalid():
    """Test parser with invalid input."""
    print("Testing Parser with invalid input...")
    preprocessor = Preprocessor()
    language = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)

    # Invalid program (missing semicolon after program name)
    # Note: Language only supports letters a, b, c, d, l, f
    source = "program abc var a : integer ;"
    tokens = preprocessor.process_string(source)
    parser = Parser(language, tokens)
    result = parser.parse()

    if not result.accepted:
        print(f"  ✓ Correctly rejected invalid input")
        print(f"    Error: {result.error_message}")
    else:
        print("  ✗ FAILED: Should have rejected invalid input")
    print()

def test_language():
    """Test Language class."""
    print("Testing Language class...")
    language = Language('Program', PARSING_TABLE, SYMBOL_INDICES, RESERVED_WORDS)
    
    # Test methods
    print(f"  ✓ Start symbol: {language.get_starting_state()}")
    print(f"  ✓ Reserved words: {language.get_reserved_words()}")
    print(f"  ✓ 'program' is reserved: {language.is_reserved_word('program')}")
    print(f"  ✓ 'xyz' is reserved: {language.is_reserved_word('xyz')}")
    
    # Test parsing table lookup
    production = language.get_control_chars('Expression', 'a')
    print(f"  ✓ Table lookup: Expression + 'a' → {production}")
    print()

if __name__ == '__main__':
    print("=" * 60)
    print("Quick Test Suite for Mini Compiler")
    print("=" * 60)
    print()
    
    try:
        test_preprocessor()
        test_language()
        test_parser_valid()
        test_parser_invalid()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
