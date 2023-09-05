from lark import Lark,Transformer,v_args
from lark.tree import Tree
json_parser = Lark(r"""
    new_rule:"{""resource" ":" "{" WORD ":" "{" WORD 
    ?value: dict
          | list
          | string
          | SIGNED_NUMBER      -> number
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value
    WORD: /[a-zA-Z_][a-zA-Z0-9_]/

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='new_rule')

with open('main.tf.json','r') as myfile:
    obj=myfile.read()

tree=json_parser.parse(obj)

# Define a transformer to convert the JSON tree to Terraform language
@v_args(inline=True)
class TerraformTransformer(Transformer):
    def __init__(self):
        self.current_child_index = -1

    def new_rule(self,items):
        print(items)

    def pair(self, key, value):
        self.current_child_index += 1
        subtree = Tree('pair', [key,value])
        for child in subtree.iter_subtrees():
            print(child)
        # if self.next_sibling:
        #     result += str(self.next_sibling)
        # return result
        # # next_node = self.children[self.current_child_index+1]
        return f'{key} = {value}\n'
        

    def string(self, value):
        return f'"{value[1:-1]}"'

    def number(self, value):
        return str(value)

    def true(self, _):
        return 'true'

    def false(self, _):
        return 'false'

    def null(self, _):
        return 'null'

    def list(self, *args):
        return '[\n' + ',\n'.join(args) + '\n]'

    def dict(self, *args):
        return '{\n' + ''.join(args) + '}\n'
    
transformer = TerraformTransformer()
result = transformer.transform(tree)

with open('example2.tf', 'w') as f:
    f.write(result)