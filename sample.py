import json
from lark import Lark, Transformer, v_args


json_grammar = r"""
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

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""

# Define a transformer to convert the JSON tree to Terraform language
@v_args(inline=True)
class TerraformTransformer(Transformer):
    def pair(self, key, value):
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


# Load the JSON file
with open('main.tf.json') as f:
    data = json.load(f)

# Parse the JSON file using the Lark parser
parser = Lark(json_grammar,start="value")
tree = parser.parse(json.dumps(data))

# Evaluate the tree using the transformer and generate the Terraform file
transformer = TerraformTransformer()
result = transformer.transform(tree)
with open('example.tf', 'w') as f:
    f.write(result)
