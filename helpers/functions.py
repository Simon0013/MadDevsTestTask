from helpers.stack import Stack

possible_tags = ['p', 'b', 'strong', 'i', 'ul', 'ol', 'div', 'span']


def get_html_block(tag: str, content: str) -> str:
    return '<{}>{}</{}>'.format(tag, content, tag)


def get_end_of_block(stack: Stack) -> str:
    result = ''
    for element in stack.get_iterator():
        result += '</{}>'.format(element)
    return result


def get_begin_of_block(stack: Stack) -> str:
    result = ''
    iterator = reversed(list(stack.get_iterator()))
    for element in iterator:
        result += '<{}>'.format(element)
    return result


def remove_substring_from_end(string: str, expr: str) -> str:
    if not string.endswith(expr):
        return string
    position = len(string) - len(expr)
    return string[:position]
