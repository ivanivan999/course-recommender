# filepath: /Users/ivanyu/Desktop/GNG_5125/assignment/ass5_chatbot/course-recommender/src/main.py
from fastapi import FastAPI, Query
from typing import List, Dict, Any
from .services.recommender import recommend_highlighted_courses

app = FastAPI(
    title="Course Recommender API",
    description="API for recommending courses based on user queries",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Course Recommender API!"}

@app.get("/recommend/", response_model=List[Dict[str, Any]])
async def recommend(
    query: str = Query(..., description="Search query for course recommendation"),
    top_n: int = Query(5, description="Number of recommendations to return")
):
    results = recommend_highlighted_courses(query, top_n)
    return results.to_dict(orient="records")