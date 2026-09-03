from app.main import app


@app.get("/healthz")
def healthz():
    return {"msg": "healthz"}


@app.get("/readyz")
def readyz():
    return {"msg": "readyz"}
