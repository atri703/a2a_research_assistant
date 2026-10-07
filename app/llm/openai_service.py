from openai import AsyncOpenAI
from app.config import settings
from app.llm.base import LLMService

class OpenAIService(LLMService):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def text(self, system: str, user: str) -> str:
        response = await self.client.responses.create(model=self.model, instructions=system, input=user)
        return response.output_text

    async def structured(self, system: str, user: str, schema):
        response = await self.client.responses.parse(model=self.model, instructions=system, input=user, text_format=schema)
        return response.output_parsed
