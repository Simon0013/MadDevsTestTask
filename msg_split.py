from bs4 import BeautifulSoup
from collections.abc import Generator

from helpers import *

MAX_LEN = 4096


def split_message(source: str, max_len=MAX_LEN) -> Generator[str]:
    if len(source) <= max_len:
        yield source
    else:
        current_length = 0
        tags_stack = Stack()
        fragment = ''
        soup = BeautifulSoup(source, 'html.parser')

        def recursive_get_fragments(elem, fragm: str, dop_part: str) -> Generator[str]:
            nonlocal current_length
            try:
                children = elem.findChildren(recursive=False)
                end_fragm = get_end_of_block(tags_stack)
                tags_stack.push(elem.name)
                tmp_element = '<{}>'.format(elem.name)
                if current_length + len(tmp_element) >= max_len:
                    yield fragm + dop_part + end_fragm
                else:
                    current_length += len(tmp_element)
                    tmp_element = dop_part + tmp_element
                    for child in children:
                        string = str(child)
                        end_of_block = get_end_of_block(tags_stack)
                        html_block = fragm + tmp_element + string + end_of_block
                        if len(html_block) <= max_len:
                            tmp_element += string
                            current_length += len(string)
                        else:
                            if (not child.name) or (child.name not in possible_tags):
                                fragm += tmp_element + end_of_block
                                yield fragm
                                tmp_element = get_begin_of_block(tags_stack) + string
                                fragm = ''
                                current_length = len(tmp_element)
                            else:
                                last_fragment = ''
                                for fr in recursive_get_fragments(child, fragm, tmp_element):
                                    if last_fragment:
                                        yield last_fragment
                                    if not fr:
                                        break
                                    last_fragment = fr
                                if not last_fragment:
                                    raise FragmentException("Не удалось разделить элемент: {}".format(child))
                                fragm = ''
                                tmp_element = remove_substring_from_end(last_fragment, get_end_of_block(tags_stack))
                                current_length = len(tmp_element)
                    fragm += tmp_element + get_end_of_block(tags_stack)
                    tags_stack.pop()
                    yield fragm
            except AttributeError as e:
                raise FragmentException('Не удалось разделить элемент: {}'.format(e))
            except FragmentException as e:
                raise e

        for element in soup.childGenerator():
            str_element = str(element)
            length = len(str_element)
            if current_length + length <= max_len:
                current_length += length
                fragment += str_element
            else:
                if (not element.name) or (element.name not in possible_tags):
                    if not fragment:
                        raise FragmentException("Невозможно разделить элемент {}, т.к. он не является HTML-блоком, "
                                                "или этот блок нельзя разделять".format(element))
                    yield fragment
                    current_length = length
                    fragment = str_element
                else:
                    last_frag = ''
                    for frag in recursive_get_fragments(element, fragment, ''):
                        if last_frag:
                            yield last_frag
                        if not frag:
                            break
                        last_frag = frag
                    if not last_frag:
                        raise FragmentException('Не удалось разделить элемент: {}'.format(element))
                    fragment = last_frag
                    current_length = len(fragment)
        yield fragment
