from pydantic import BaseModel

class User(BaseModel):
    discord_id: str
    username: str

class TrackedProduct(BaseModel):
    product_id: str
    title: str
    mrp: str
    discount_percentage: str
    current_price: str
    categories: list[str]
    description: list[str]
    rating: str
    domain: str
    image: str

class ScheduledTask(BaseModel):
    task_id: str
    user_id: User
    task_status: str
    task_output: list[TrackedProduct]