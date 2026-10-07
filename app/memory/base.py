from abc import ABC, abstractmethod
from typing import Any

class MemoryStore(ABC):
    @abstractmethod
    async def get(self, project_id: str) -> dict[str, Any] | None: ...
    @abstractmethod
    async def set(self, project_id: str, value: dict[str, Any]) -> None: ...
