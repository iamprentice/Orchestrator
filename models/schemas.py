from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EmotionalIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class Complaint(BaseModel):
    title: str = Field(description="Short title summarizing the complaint")
    description: str = Field(description="Detailed description of the complaint")
    frequency: int = Field(description="Estimated monthly mentions across platforms")
    emotional_intensity: EmotionalIntensity
    example_quotes: List[str] = Field(description="Real-sounding example quotes from users")
    affected_user_segments: List[str] = Field(description="User types most affected")


class ExistingSolution(BaseModel):
    name: str
    description: str
    limitations: List[str]
    market_share: Optional[str] = None


class MarketGap(BaseModel):
    description: str
    unsolved_complaints: List[str]
    why_existing_solutions_fail: str
    estimated_market_size: str


class MarketOpportunity(BaseModel):
    total_addressable_market: str
    serviceable_addressable_market: str
    growth_rate: str
    urgency: str


class ComplaintAnalysis(BaseModel):
    product_category: str
    top_complaints: List[Complaint]
    existing_solutions: List[ExistingSolution]
    market_gaps: List[MarketGap]
    market_opportunity: MarketOpportunity
    data_sources_analyzed: List[str]
    summary: str = Field(description="Executive summary of findings")


class StartupOpportunity(BaseModel):
    name: str = Field(description="Startup/product name")
    one_liner: str = Field(description="One sentence pitch")
    problem: str
    solution: str
    target_users: List[str]
    key_differentiators: List[str]
    estimated_revenue_potential: str
    difficulty_to_build: str = Field(description="Easy / Medium / Hard / Very Hard")
    time_to_market: str = Field(description="Estimated time to launch MVP")
    confidence_score: int = Field(description="Confidence score 1-100 based on complaint data")


class PricingTier(BaseModel):
    name: str
    price: str
    features: List[str]
    target_user: str


class MVPSpec(BaseModel):
    opportunity_name: str
    problem_statement: str
    core_features: List[str]
    tech_stack_recommendation: str
    timeline: str
    pricing_model: List[PricingTier]
    go_to_market: List[str]
    key_metrics: List[str]
    competitor_analysis: List[str]
    marketing_angles: List[str]
    success_criteria: List[str]
    week_one_actions: List[str] = Field(description="Concrete first-week action items")
