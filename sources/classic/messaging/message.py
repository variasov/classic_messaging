from typing import Any

import attr


@attr.dataclass
class Message:
    target: str
    body: Any
