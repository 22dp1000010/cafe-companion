from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MenuItem(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    prepTimeMinutes: int


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    preferences: Optional[List[str]] = []
    order_history: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    opted_in_matching: bool = False


class Order(BaseModel):
    id: str
    user_id: str
    items: List[str]
    status: str  # queued, in_progress, ready, completed
    created_at: datetime
    estimated_ready_time: Optional[str] = None
    total_price: float


class Interest(BaseModel):
    user_id: str
    tags: List[str]


class Match(BaseModel):
    id: str
    user_1_id: str
    user_2_id: str
    common_interests: List[str]
    score: float
    created_at: datetime


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    order_intent: Optional[dict] = None
    recommendation: Optional[str] = None


class WaitTimeResponse(BaseModel):
    estimated_wait_minutes: int
    queue_size: int
    baristas_available: int
