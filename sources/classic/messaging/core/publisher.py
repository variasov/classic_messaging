from abc import ABC, abstractmethod
import threading

from .message import Message


class Publisher(ABC):

    def __attrs_post_init__(self):
        self._local = threading.local()

    @abstractmethod
    def publish(self, *messages: Message):
        pass

    @property
    def _deferred(self):
        if not hasattr(self._local, 'messages'):
            self._local.messages = []
        return self._local.messages

    def plan(self, *messages: Message):
        self._deferred.extend(messages)

    def flush(self):
        self.publish(*self._deferred)
        self.reset()

    def reset(self):
        if hasattr(self._local, 'messages'):
            del self._local.messages
