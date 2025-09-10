from uuid import UUID
from pydantic import BaseModel, Field


class OrderStatusRequest(BaseModel):
    order_id: str = Field(
        ...,
        description="The ID of the order to check status for.",
        examples=["order_1", "order_2"]
    )

class ProductInfoRequest(BaseModel):
    product_id: str = Field(
        ...,
        description="The ID of the product to get information about.",
        examples=["123", "456"]
    )

class ChatRequest(BaseModel):
    session_id: UUID = Field(
        default_factory=UUID,
        description="A unique identifier for the chat session. If not provided, a new UUID will be generated."
    )
    user_input: str = Field(
        ...,
        description="The user's input message to the chat system.",
        examples=["Hello, how are you?", "What's the weather like today?"]
    )

class ChatResponse(BaseModel):
    session_id: str
    ai_response: str