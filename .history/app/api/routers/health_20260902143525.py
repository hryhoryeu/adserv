from app.main import app


@app.get("/healthz")
def healthz():
    return
