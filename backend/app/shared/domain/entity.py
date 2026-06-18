from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass(kw_only=True)
class Entity:
    id: Optional[Any] = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    _domain_events: List[Any] = field(default_factory=list, init=False)

    def add_domain_event(self, event: Any) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    @property
    def domain_events(self) -> List[Any]:
        return self._domain_events.copy()









































