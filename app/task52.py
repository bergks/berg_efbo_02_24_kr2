from fastapi import FastAPI, Cookie, Response, HTTPException, status
from itsdangerous import Signer, BadSignature
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "my-secret-key"
signer = Signer(SECRET_KEY)


class LoginData(BaseModel):
    username: str
    password: str


users = [
    {"username": "user", "password": "123"}
]


def verify_user(username: str, password: str) -> bool:
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False


@app.post('/login')
def login(login_data: LoginData, response: Response):
    if not verify_user(login_data.username, login_data.password):
        return {'error': 'Invalid credentials'}
    signed_token = signer.sign(login_data.username).decode()

    response.set_cookie(
        key="session_token",
        value=signed_token,
        max_age=3600,
        httponly=True
    )

    return {"message": "Login successful"}


@app.get('/user')
def get_user(session_token: str | None = Cookie(default=None)):
    if not session_token:
        return {'error': 'Missing token'}

    try:
        username = signer.unsign(session_token).decode()
    except BadSignature:
        return {'error': 'Invalid token'}

    if not any(user["username"] == username for user in users):
        return {'error': 'User not found'}

    return {
        "username": username,
        "message": "Welcome to your profile"
    }