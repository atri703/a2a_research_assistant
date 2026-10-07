from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LLMService(ABC):
    @abstractmethod
    async def text(self, system: str, user: str) -> str: ...

    @abstractmethod
    async def structured(self, system: str, user: str, schema: type[T]) -> T: ...
