from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pydantic.generics import GenericModel
from transitions import Machine


@dataclass(eq=True, frozen=True)
class StorageKey:
    chat_id: int
    user_id: int


StateData = TypeVar('StateData', bound=BaseModel)

class MemoryStorageRecord(GenericModel, Generic[StateData]):
    data: StateData | None
    state: Machine

    class Config:
        arbitrary_types_allowed = True


class InMemoryStorage(Generic[StateData]):
    def __init__(self):
        self._states: dict[StorageKey, MemoryStorageRecord] = {}

    def get_entry(self, key: StorageKey) -> MemoryStorageRecord | None:
        return self._states.get(key, None)

    def add_entry(
        self,
        key: StorageKey,
        state_machine: Machine,
        data: StateData | None = None
    ) -> None:
        self._states[key] = MemoryStorageRecord(
            state=state_machine,
            data=data
        )

    def clear_entry(
        self,
        key: StorageKey
    ) -> None:
        if key not in self._states:
            return

        del self._states[key]
