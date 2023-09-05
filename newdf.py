import pandas as pd
import json

# create a sample dataframe
df = pd.DataFrame({'A': [1, 2, 3], 'B': ['{"key1": "value1", "key2": "value2"}', '{"key3": "value3", "key4": "value4"}', '{"key5": "value5", "key6": "value6"}']})

# use apply to convert the strings to JSON format
df['B'] = df['B'].apply(json.loads)

# print the dataframe
print(df)
