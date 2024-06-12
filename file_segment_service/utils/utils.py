import ast


def extract_file_structure(source_code: str) -> list[dict]:
    return [
        {
            "start_line": node.lineno,
            "end_line": node.end_lineno,
        }
        for node in ast.iter_child_nodes(ast.parse(source_code))
    ]
