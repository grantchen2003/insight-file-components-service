import ast


def extract_file_component_content_and_lines(source_code: str) -> list[dict]:
    file_component_content_and_lines = []
    for node in ast.iter_child_nodes(ast.parse(source_code)):
        start_line = node.lineno
        end_line = node.end_lineno
        content = "\n".join(source_code.splitlines()[node.lineno - 1 : node.end_lineno])
        
        file_component_content_and_lines.append((start_line, end_line, content))

    return file_component_content_and_lines


def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened
