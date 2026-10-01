from abc import ABC, abstractmethod

from pydantic import BaseModel


class NormalizedCard(BaseModel):
    external_id: str
    name: str
    set_id: str
    set_name: str
    card_number: str
    rarity: str | None = None
    supertype: str | None = None
    subtypes: list[str] = []
    image_small: str | None = None
    image_large: str | None = None
    language: str = "EN"


class CardProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> list[NormalizedCard]: ...

    @abstractmethod
    async def get_by_id(self, external_id: str) -> NormalizedCard | None: ...
