import json
from typing import Any
from redis.asyncio import Redis
from app.config import settings
from app.memory.base import MemoryStore

class RedisMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self.client = Redis.from_url(settings.redis_url, decode_responses=True)
    def _key(self, project_id: str) -> str:
        return f"research:project:{project_id}:state"
    async def get(self, project_id: str) -> dict[str, Any] | None:
        raw = await self.client.get(self._key(project_id))
        return json.loads(raw) if raw else None
    async def set(self, project_id: str, value: dict[str, Any]) -> None:
        await self.client.set(self._key(project_id), json.dumps(value))
