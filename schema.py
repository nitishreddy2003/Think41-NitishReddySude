# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    """Schema for the user's request."""
    message: str = Field(..., min_length=1, description="The message from the user.")
    session_id: Optional[int] = Field(None, description="The existing session ID to continue a conversation.")

class ChatResponse(BaseModel):
    """Schema for the AI's response."""
    reply: str
    session_id: int