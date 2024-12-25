from collections import deque
from collections.abc import Generator


class Stack:
    def __init__(self):
        self.__deq = deque()

    def push(self, element: str):
        self.__deq.appendleft(element)

    def pop(self) -> str:
        return self.__deq.popleft()

    def get_iterator(self) -> Generator[str]:
        for element in self.__deq:
            yield element
