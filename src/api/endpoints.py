from fastapi import APIRouter
from typing import List
from src.services.recommender import recommend_highlighted_courses
from src.api.models import CourseRecommendation

router = APIRouter()

@router.get("/recommend_highlighted/", response_model=List[CourseRecommendation])
async def recommend_highlighted(query: str, top_n: int = 5):
    recommendations = recommend_highlighted_courses(query, top_n)
    return recommendations.to_dict(orient="records")