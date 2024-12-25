from msg_split import split_message

filepath = 'src/source.html'
max_len = 4096


def test_check_than_all_fragments_not_more_than_max_len():
    with open(filepath, 'r') as f:
        for fragment in split_message(f.read(), max_len):
            assert len(fragment) <= max_len


def test_check_than_all_fragments_not_empty():
    with open(filepath, 'r') as f:
        for fragment in split_message(f.read(), max_len):
            assert len(fragment) > 0
