from lark import Lark, Transformer, v_args

grammar = r"""
start: value
value: object | array | string | SIGNED_INT | FLOAT | "true" -> true | "false" -> false | "null" -> null
object: "{" [pair ("," pair)*] "}"
pair: string ":" value
array: "[" [value ("," value)*] "]"
string: ESCAPED_STRING
%import common.ESCAPED_STRING
%import common.SIGNED_INT
%import common.FLOAT
%import common.WS
%ignore WS
"""

@v_args(inline=True)
class JsonToHashicorpTransformer(Transformer):
    def string(self, s):
        return s[1:-1]
        
    def object(self, pairs):
        d = dict(pairs)
        if "resource" in d and isinstance(d["resource"], dict):
            resource_name = next(iter(d["resource"]))
            resource_properties = d["resource"][resource_name]
            return f"resource \"{resource_name}\" {{\n{self.indent(self.hashicorp_properties(resource_properties))}}}"
        else:
            return ""

    def hashicorp_properties(self, props):
        pairs = []
        for k, v in props.items():
            if isinstance(v, dict):
                pairs.append((k, f"{{\n{self.indent(self.hashicorp_properties(v))}}}\n"))
            else:
                pairs.append((k, f'"{v}"'))
        return "".join([f"{k} = {v}\n" for k, v in pairs])

    def array(self, items):
        return []

    def true(self):
        return True

    def false(self):
        return False

    def null(self):
        return None
        
    def indent(self, s):
        return "  " + s.replace("\n", "\n  ")

json_parser = Lark(grammar, parser="lalr", transformer=JsonToHashicorpTransformer())

json_str = '{"resource": {"aws_instance": {"example": {"instance_type": "t2.micro", "ami": "ami-abc123"}}}}'
hashicorp_str = json_parser.parse(json_str)
print(hashicorp_str)
