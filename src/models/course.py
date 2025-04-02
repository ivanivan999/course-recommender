from pydantic import BaseModel

class Course(BaseModel):
    title: str
    category: str
    rating: float
    viewers: int