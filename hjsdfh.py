from lark import Lark

parser = Lark(r"""
?start: NAME "=" possible_values
possible_values: "apple" | "banana" | "orange"
NAME: /\w+/
%ignore /\s+/
""", parser="lalr")

interactive = parser.parse_interactive("my_variable = ")

# feeds the text given to above into the parsers. This is not done automatically.
interactive.exhaust_lexer()


# returns the names of the Terminals that are currently accepted.
print(interactive.accepts())