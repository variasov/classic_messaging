from abc import ABC, abstractmethod
from contextlib import ContextDecorator

from classic.components import component

from .message import Message
from .utils import ThreadSafeCounter, LocalList


@component
class Publisher(ContextDecorator, ABC):

    def __attrs_post_init__(self):
        self.deferred = LocalList()
        self.calls = ThreadSafeCounter()

    @abstractmethod
    def publish(self, *messages: Message):
        pass

    def plan(self, *messages: Message):
        self.deferred.extend(messages)

    def on_finish(self):
        pass

    def flush(self):
        for entity in self.deferred:
            self.publish(entity)

        self.reset()

    def reset(self):
        self.deferred.clear()

    def __enter__(self):
        self.calls.increment()
        return self

    def __exit__(self, *exc):
        self.calls.decrement()

        if self.calls.is_last:
            if exc[0] is None:
                self.flush()
            else:
                self.reset()

            self.on_finish()

        return False
