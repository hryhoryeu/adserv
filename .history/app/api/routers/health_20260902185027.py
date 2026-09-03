from app.main import app
from app.config import config


@app.get("/healthz")
def healthz():
    return {"msg": "healthz"}


@app.get("/readyz")
def readyz():
    return {"msg": "readyz"}
