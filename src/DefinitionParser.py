import re


def parse_def(string, function_names):
    pattern = r"\s*([A-Z]\w+)\s*\(\s*(.+)\s*\)\s*"
    match = re.search(pattern, string)
    if match is None:
        return None
    results = match.groups()
    if (results[0] not in function_names) or len(results) != 2:
        return None
    arguments_str = results[1].strip().replace(' ', '')
    arguments = arguments_str.split(',')
    return results[0], arguments


if __name__ == '__main__':
    print(parse_def('Linestring (A, B)', ['Linestring', 'Segment']))
