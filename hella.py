from lark import Lark, Transformer

grammar = r'''
start: "{" pair ("," pair)* "}"
pair: string ":" (string | "{" pair ("," pair)* "}")

string: ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
'''

class JsonTransformer(Transformer):
    def start(self, items):
        return dict(items)

    def pair(self, items):
        return (items[0], items[1])

    def string(self, s):
        return s[1:-1]

    def dict(self, items):
        result = {}
        for k, v in items.children:
            result[k.value] = v.children[0]
        return result

parser = Lark(grammar, parser='lalr', transformer=JsonTransformer())
tree = parser.parse('{"key1": "value1", "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"}}')
result = tree.pretty()
print(result)
