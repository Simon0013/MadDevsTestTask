from argparse import ArgumentParser
from msg_split import split_message


def create_parser() -> ArgumentParser:
    _parser = ArgumentParser()
    _parser.add_argument('--max-len')
    _parser.add_argument('filepath', nargs='?', default='src/source.html')
    return _parser


parser = create_parser()
namespace = parser.parse_args()
with open(namespace.filepath, 'r') as f:
    content = f.read()
    result = split_message(content, int(namespace.max_len))
    for i, fragment in enumerate(result):
        print('-- fragment #{}: {} chars. --'.format(i+1, len(fragment)))
        print(fragment)
