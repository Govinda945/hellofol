from lark import Lark, Transformer, v_args

from lark.visitors import Interpreter

# Define a Lark grammar for a simple calculator language
calc_grammar = r"""
    ?start: sum
    ?sum: product (("+" | "-") product)*
    ?product: atom (("*" | "/") atom)*
    ?atom: NUMBER | "(" sum ")"
    NUMBER: /\d+(\.\d+)?/
    %import common.WS
    %ignore WS
"""

# Define a Transformer class to convert the parse tree to an abstract syntax tree (AST)
class CalcTransformer(Transformer):
    @v_args(inline=True)
    def NUMBER(self, n):
        return float(n)

    def sum(self, *args):
        if len(args) == 1:
            return args[0]
        else:
            result = args[0]
            for i in range(1, len(args), 2):
                op = args[i]
                operand = args[i+1]
                if op == "+":
                    result += operand
                elif op == "-":
                    result -= operand
            return result

    def product(self, *args):
        if len(args) == 1:
            return args[0]
        else:
            result = args[0]
            for i in range(1, len(args), 2):
                op = args[i]
                operand = args[i+1]
                if op == "*":
                    result *= operand
                elif op == "/":
                    result /= operand
            return result

# Define a program to evaluate using the calculator language
program = "1 + 2 * (3 - 4) / 5"

# Parse the program using the calculator grammar
parser = Lark(calc_grammar, parser='lalr', transformer=CalcTransformer())
tree = parser.parse(program)

# Evaluate the program using the interpreter
interpreter = Interpreter()
result = interpreter.visit(tree)
print(result)  # Output: 1.2
