import ast


def extract_file_components(source_code: str) -> list[dict]:
    return [
        {
            "start_line": node.lineno,
            "end_line": node.end_lineno,
        }
        for node in ast.iter_child_nodes(ast.parse(source_code))
    ]


def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened
