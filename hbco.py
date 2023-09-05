def extract_keys(d, level=0, max_level=3):
    """
    Recursively extract the first `max_level` keys from a nested dictionary `d`.
    """
    if level >= max_level:
        return []

    keys = []
    for k, v in d.items():
        keys.append(k)
        if isinstance(v, dict):
            nested_keys = extract_keys(v, level=level+1, max_level=max_level)
            keys.extend(nested_keys)

        if len(keys) >= max_level:
            break

    return keys[:max_level]


nested_dicts = [
    {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': 4},
    {'h': {'i': {'j': 5, 'k': 6}, 'l': 7}, 'm': 8}

]

keys = [extract_keys(d) for d in nested_dicts]

print(keys)  # Output: [['a', 'b', 'c'], ['h', 'i', 'j']]
