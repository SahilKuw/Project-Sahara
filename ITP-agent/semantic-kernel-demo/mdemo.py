from typing import TypedDict

class LightModel(TypedDict):
    id: int
    name: str
    is_on: bool | None
    brightness: int | None
    hex: str | None