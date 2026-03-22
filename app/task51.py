from fastapi import FastAPI, Cookie, Response
from uuid import uuid4

app = FastAPI()

users = [
    {'username': 'user', 'password': '123'}
]

sessions = {}

def verify_user(username, password):
    for user in users:
        if user.get('username') == username\
            and user.get('password') == password:
            return True
    return None


@app.post('/login')
def login(username: str, password: str, response: Response):
    user = verify_user(username, password)
    if user:
        session_id = uuid4()
        response.set_cookie(key='session_token', value=f'{session_id}', max_age=3600, httponly=True)
        sessions[f'{session_id}'] = username
        return {'message': 'Login successful', 'token': session_id}
    return {'error': 'User not found'}

@app.get('/user')
def get_user(session_token: str | None = Cookie(default=None)):
    if session_token:
        if session_token in sessions:
            return {'user': sessions[f'{session_token}']}
        return {'error': 'Invalid token'}
    return {'error': 'Unauthorized'}