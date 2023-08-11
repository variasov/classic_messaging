import threading
from typing import Any, Dict, Iterable


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


class UnsafeThreadLocal:

    @property
    def _storage(self) -> Dict[str, Any]:
        current_thread = threading.current_thread()
        if not hasattr(current_thread, 'unsafe_storage'):
            setattr(current_thread, 'unsafe_storage', {})
        return current_thread.unsafe_storage

    def __getattribute__(self, item):
        try:
            return self._storage[item]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self._storage[key] = value

    def __delattr__(self, item):
        del self._storage[item]
