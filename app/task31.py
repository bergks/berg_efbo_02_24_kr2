from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI

app = FastAPI()

class UserCreate (BaseModel):
    name: str
    email: EmailStr
    age: int | None = Field(None, gt=0)
    is_subscribed: bool = False

@app.post('/create_user')
def create_user(user: UserCreate):
    return user


