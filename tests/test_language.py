"""Tests for the Language class."""

import pytest

from mini_compiler.core.language import Language


class TestLanguage:
    """Test suite for Language class."""

    def test_initialization(self, language):
        """Test that Language initializes correctly."""
        assert language is not None
        assert language.get_starting_state() == "Program"

    def test_get_starting_state(self, language):
        """Test get_starting_state method."""
        start = language.get_starting_state()

        assert start == "Program"
        assert isinstance(start, str)

    def test_get_indexes(self, language):
        """Test get_indexes returns symbol mapping."""
        indexes = language.get_indexes()

        assert isinstance(indexes, dict)
        assert len(indexes) > 0

        # Check some expected symbols
        assert "program" in indexes
        assert "Program" in indexes
        assert "begin" in indexes
        assert "end" in indexes

    def test_get_control_chars_valid(self, language):
        """Test get_control_chars with valid non-terminal and terminal."""
        # Expression + identifier should give production
        production = language.get_control_chars("Expression", "a")

        assert production is not None
        assert isinstance(production, str)
        assert len(production) > 0

    def test_get_control_chars_epsilon(self, language):
        """Test get_control_chars returns lambda for epsilon productions."""
        # ExpressionTail + semicolon should be epsilon
        production = language.get_control_chars("ExpressionTail", ";")

        assert production == "lambda"

    def test_get_control_chars_error(self, language):
        """Test get_control_chars returns empty string for invalid combinations."""
        # Invalid combination should return empty string
        production = language.get_control_chars("Expression", ")")

        assert production == ""

    def test_is_reserved_word(self, language):
        """Test is_reserved_word method."""
        assert language.is_reserved_word("program") is True
        assert language.is_reserved_word("var") is True
        assert language.is_reserved_word("begin") is True
        assert language.is_reserved_word("end") is True
        assert language.is_reserved_word("integer") is True
        assert language.is_reserved_word("print") is True

        # Not reserved
        assert language.is_reserved_word("foo") is False
        assert language.is_reserved_word("abc") is False

    def test_get_reserved_words(self, language):
        """Test get_reserved_words returns a set."""
        reserved = language.get_reserved_words()

        assert isinstance(reserved, set)
        assert "program" in reserved
        assert "var" in reserved
        assert "begin" in reserved
        assert "end" in reserved
        assert "integer" in reserved
        assert "print" in reserved

    def test_reserved_words_immutable(self, language):
        """Test that get_reserved_words returns a copy (not modifiable)."""
        reserved1 = language.get_reserved_words()
        reserved1.add("test")

        reserved2 = language.get_reserved_words()

        # Original should not be modified
        assert "test" not in reserved2
