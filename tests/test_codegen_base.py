"""Tests for base code generator."""

import pytest

from mini_compiler.codegen.base import CodeGenerator
from mini_compiler.core.ast_nodes import Assignment, Number, Program, Variable


class TestCodeGeneratorBase:
    """Test suite for CodeGenerator base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that CodeGenerator cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CodeGenerator()

    def test_concrete_implementation(self):
        """Test that a concrete implementation can use base functionality."""

        class TestGenerator(CodeGenerator):
            """Test concrete generator."""

            def visit_program(self, node):
                return f"Program: {node.name}"

            def visit_declaration(self, node):
                return f"Decl: {', '.join(node.names)}"

            def visit_assignment(self, node):
                return f"Assign: {node.variable}"

            def visit_print(self, node):
                return f"Print: {node.variable}"

            def visit_binary_expression(self, node):
                return f"BinOp: {node.operator}"

            def visit_number(self, node):
                return str(node.value)

            def visit_variable(self, node):
                return node.name

        # Create test generator
        gen = TestGenerator()

        # Test _emit functionality
        gen._emit("test line")
        assert "test line" in gen._output

        # Test _emit_blank
        gen._emit_blank()
        assert "" in gen._output

        # Test indentation
        gen._indent()
        gen._emit("indented")
        gen._dedent()

        # Check indented output in internal buffer
        assert any("    indented" in line for line in gen._output)

    def test_visitor_pattern_integration(self):
        """Test that visitor pattern works with AST nodes."""

        class SimpleGenerator(CodeGenerator):
            """Simple test generator."""

            def visit_program(self, node):
                return "program"

            def visit_declaration(self, node):
                return "declaration"

            def visit_assignment(self, node):
                expr = node.expression.accept(self)
                return f"{node.variable} = {expr}"

            def visit_print(self, node):
                return "print"

            def visit_binary_expression(self, node):
                return "binop"

            def visit_number(self, node):
                return str(node.value)

            def visit_variable(self, node):
                return node.name

        gen = SimpleGenerator()

        # Create simple AST nodes
        num = Number(42)
        var = Variable("x")

        # Visit nodes
        assert gen.visit_number(num) == "42"
        assert gen.visit_variable(var) == "x"

        # Test assignment with expression
        assignment = Assignment("a", num)
        result = gen.visit_assignment(assignment)
        assert result == "a = 42"
