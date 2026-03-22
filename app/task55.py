from fastapi import FastAPI, Header, Depends, Response
from datetime import datetime

app = FastAPI()

def get_common_headers(
    user_agent: str = Header(...),
    accept_language: str = Header(...)
):
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

@app.get('/headers')
def get_headers(headers: dict = Depends(get_common_headers)):
    return headers

@app.get('/info')
def get_info(response: Response, headers: dict = Depends(get_common_headers)):
    response.headers['X-Server-Time'] = datetime.now().isoformat()
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": headers
    }