import re

string = "{'hello'{'b'{'c'{'d': python"
regex = r"\{\'\w+\'\{\'\w+\'\{\'\w+\'\{\'\w+\':"

match = re.search(regex, string)
if match:
    print("Match found:", match.group())
else:
    print("Match not found.")
