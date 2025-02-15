from pydantic import BaseModel

class Polzovatel(BaseModel):
    name: str
    id: int


