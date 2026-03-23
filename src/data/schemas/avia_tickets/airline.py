from pydantic import BaseModel, TypeAdapter


class NameTranslations(BaseModel):
    en: str

class Airline(BaseModel):
    name_translations: NameTranslations
    code: str
    name: str | None
    is_lowcost: bool


airlines_adapter = TypeAdapter(list[Airline])
