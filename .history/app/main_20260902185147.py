from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI()


app = create_app()
app.add_api_route()
