# Classic Messaging

This package provides abstract classes for message queues.

Usage:

```python
from classic.components import component
from classic.messaging import Message, Publisher


@component
class SomeService:
    publisher: Publisher

    def do_some_work(self):
        message = Message('target', 'Some very useful info')
        self.publisher.publish(message)
```

Publisher have inner buffer. Messages can be planned for publishing, and 
will be published later

Usage with deferred publishing:

```python
from classic.components import component
from classic.messaging import Message, Publisher


@component
class SomeService:
    publisher: Publisher

    def create_message(self):
        message = Message('target', 'Some very useful info')
        self.publisher.plan(message)

    def do_some_work(self):
        try:
            self.create_message()
        except Exception:
            self.publisher.reset_deferred()
            raise
        else:
            self.publisher.flush()
```


Usage with join_points:
```python
from classic.components import component
from classic.messaging import Message, Publisher
from classic.aspects import join_poin


@component
class SomeService:
    publisher: Publisher
    
    @join_poin
    def do_some_work(self):
        message = Message('target', 'Some very useful info')
        self.publisher.plan(message)

        
class RealPublisher(Publisher):
    
    def publish(self, message):
        print(message)


publisher = RealPublisher()

SomeService.do_some_work.join(publisher)
```