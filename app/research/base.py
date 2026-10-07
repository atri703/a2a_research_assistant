from abc import ABC, abstractmethod
from app.schemas.models import EvidenceItem

class ResearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 8) -> list[EvidenceItem]: ...
