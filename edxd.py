from lark import Lark, Transformer
from lark.tree import Tree

grammar = '''
start: pair+
pair: key "=" value
key: /[a-zA-Z_][a-zA-Z0-9_]*/
value: ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
'''

class TerraformTransformer(Transformer):
    def pair(self, pair):
        key, value = pair
        subtree = Tree('pair', [key,value])
        for child in subtree.iter_subtrees():
            print(child)
        # return f'{key} = {value}\n'

parser = Lark(grammar, parser='lalr', transformer=TerraformTransformer())

tree = parser.parse('''
foo = "bar"
baz = "qux"
''')
