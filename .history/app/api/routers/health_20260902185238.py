from app.config import config
from app.main import app


@app.get("/healthz")
async def healthz():
    return {"msg": f"healthz. {config.database_url}"}


@app.get("/readyz")
async def readyz():
    return {"msg": "readyz"}
