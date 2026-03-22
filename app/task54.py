from fastapi import FastAPI, Header, HTTPException, status

app = FastAPI()

@app.get('/headers')
def get_headers(
        user_agent: str | None = Header(default=None),
        accept_language: str | None = Header(default=None)
):
    if user_agent is None:
        raise HTTPException(status_code=400, detail="Missing User-Agent")
    if accept_language is None:
        raise HTTPException(status_code=400, detail="Missing Accept-Language")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }