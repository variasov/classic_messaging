import threading
from typing import Any, Iterable


class Counter:

    def __init__(self):
        self._calls_count = 0

    def increment(self):
        self._calls_count += 1

    def decrement(self):
        self._calls_count -= 1

    @property
    def is_last(self):
        return self._calls_count == 0

    @property
    def is_first(self):
        return self._calls_count == 1


class ThreadSafeCounter(Counter, threading.local):
    pass


class LocalList(threading.local):

    def __init__(self):
        self._list = []

    def append(self, element: Any):
        self._list.append(element)

    def extend(self, elements: Iterable[Any]):
        self._list.extend(elements)

    def clear(self):
        self._list.clear()

    def __iter__(self):
        return iter(self._list)
