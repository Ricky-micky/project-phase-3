# schemas.py
from pydantic import BaseModel, EmailStr

class Createuserschema(BaseModel):
    username: str
    email: EmailStr
    name: str

    class Config:
        orm_mode = True


class CreateProductSchema(BaseModel):
    name: str
    description: str = None
    price: float
    stock: int = 0
    category: str
    image_url: str

    class Config:
        orm_mode = True

class CreateOrderSchema(BaseModel):
    user_id: int
    order_date: str

    class Config:
        orm_mode = True