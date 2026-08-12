"""Pydantic models for structured data validation."""
from pydantic import BaseModel, Field
from typing import List


class CategoryScore(BaseModel):
    """Score for a single rubric category."""
    name: str = Field(description="Name of the category")
    score: float = Field(description="Points awarded for this category")
    max_score: float = Field(description="Maximum possible points for this category")
    reasoning: str = Field(description="One-sentence explanation for the score")


class AnalysisResult(BaseModel):
    """Complete analysis result with scores and recommendation."""
    categories: List[CategoryScore] = Field(description="List of category scores")
    total_score: float = Field(description="Sum of all category scores")
    biggest_leak_category: str = Field(description="Name of the weakest category")
    recommendation: str = Field(description="2-3 sentence actionable recommendation")
