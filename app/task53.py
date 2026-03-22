from fastapi import FastAPI, Cookie, Response, status
from itsdangerous import Signer, BadSignature
from pydantic import BaseModel
from uuid import uuid4
import time

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

users = [
    {"username": "user", "password": "123"}
]

SECRET_KEY = "my-secret-key"
signer = Signer(SECRET_KEY)

sessions = {}

def verify_user(username: str, password: str) -> bool:
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False


def create_signed_token(session_id: str, timestamp: int) -> str:
    payload = f"{session_id}.{timestamp}"
    return signer.sign(payload).decode()

def parse_signed_token(token: str) -> tuple[str, int]:
    try:
        payload = signer.unsign(token).decode()
        session_id, timestamp_str = payload.split('.')
        timestamp = int(timestamp_str)
        return session_id, timestamp
    except (BadSignature, ValueError):
        return None, None


@app.post('/login')
def login(login_data: LoginData, response: Response):
    if not verify_user(login_data.username, login_data.password):
        response.status_code = 401
        return {"message": "Unauthorized"}

    session_id = str(uuid4())
    current_time = int(time.time())

    sessions[session_id] = login_data.username

    signed_token = create_signed_token(session_id, current_time)

    response.set_cookie(
        key="session_token",
        value=signed_token,
        max_age=3600,
        httponly=True
    )

    return {"message": "Login successful"}


@app.get('/user')
def get_user(response: Response, session_token: str | None = Cookie(default=None)):
    if not session_token:
        response.status_code = 401
        return {"message": "Unauthorized"}

    session_id, token_time = parse_signed_token(session_token)
    if session_id is None:
        response.status_code = 401
        return {"message": "Invalid session token"}

    if session_id not in sessions:
        response.status_code = 401
        return {"message": "Session not found"}

    current_time = int(time.time())
    elapsed = current_time - token_time

    if elapsed > 300:
        del sessions[session_id]
        response.status_code = 401
        return {"message": "Session expired"}

    if elapsed >= 180:
        new_time = current_time
        new_token = create_signed_token(session_id, new_time)
        response.set_cookie(
            key="session_token",
            value=new_token,
            max_age=3600,
            httponly=True
        )
        return {"username": sessions[session_id], "message": "Session renewed"}

    return {"username": sessions[session_id], "message": "Welcome to your profile"}