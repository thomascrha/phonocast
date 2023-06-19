from pydantic import BaseModel


class Volume(BaseModel):
    volume: int
