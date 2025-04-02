from pydantic import BaseModel
from typing import List, Optional

class Course(BaseModel):
    title: str
    category: str
    rating: float
    viewers: int

class HighlightedRecommendation(BaseModel):
    query: str
    method: str
    course: Course

class HighlightedRecommendationsResponse(BaseModel):
    recommendations: List[HighlightedRecommendation]