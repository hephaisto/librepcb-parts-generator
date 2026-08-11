from os import makedirs, path

from typing import Any, Iterable, List

# String escape sequences
STRING_ESCAPE_SEQUENCES = (
    ('\\', '\\\\'),  # Must be the first one to avoid recursion!
    ('\b', '\\b'),
    ('\f', '\\f'),
    ('\n', '\\n'),
    ('\r', '\\r'),
    ('\t', '\\t'),
    ('\v', '\\v'),
    ('"', '\\"'),
)


def indent(level: int, lines: Iterable[str]) -> List[str]:
    """
    Indent the lines by the specified level.
    """
    return [' ' * level + line for line in lines]


def indent_entity(entity: Any) -> str:
    """
    Convert an entity to a string, indent every line of the string with a space,
    and add a trailing newline.

    >>> indent_entity('(foo "1")')
    ' (foo "1")\\n'
    >>> indent_entity('(bar "2"\\n (baz "3")\\n)')
    ' (bar "2"\\n  (baz "3")\\n )\\n'
    """
    result = '\n'.join(indent(1, str(entity).splitlines()))
    result += '\n'
    return result


def indent_entities(entities: Iterable[Any]) -> str:
    """
    Apply the `indent_entity` function to every item in the specified list of entities,
    and return the concatenated string.

    >>> indent_entities(['(bar "2")', '(bar "3")'])
    ' (bar "2")\\n (bar "3")\\n'
    """
    return ''.join(map(indent_entity, entities))


def escape_string(string: str) -> str:
    """
    Escape a string according to LibrePCB S-Expression escaping rules.
    """
    for search, replacement in STRING_ESCAPE_SEQUENCES:
        string = string.replace(search, replacement)
    return string


def format_float(number: float) -> str:
    """
    Format a float according to LibrePCB normalization rules.
    """
    formatted = '{:.3f}'.format(number)
    if formatted == '-0.000':
        return '0.0'  # Remove useless sign
    if formatted[-1] == '0':
        if formatted[-2] == '0':
            return formatted[:-2]
        return formatted[:-1]
    return formatted


def serialize_common(
    serializable: Any, output_directory: str, uuid: str, long_type: str, short_type: str
) -> None:
    """
    Centralized serialize() implementation shared between Component, Symbol, Device, Package
    """
    dir_path = path.join(output_directory, uuid)
    if not (path.exists(dir_path) and path.isdir(dir_path)):
        makedirs(dir_path)
    with open(path.join(dir_path, f'.librepcb-{short_type}'), 'w', newline='\n') as f:
        f.write('2\n')
    with open(path.join(dir_path, f'{long_type}.lp'), 'w', newline='\n') as f:
        f.write(str(serializable))
        f.write('\n')
