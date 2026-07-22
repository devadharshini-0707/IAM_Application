from fastapi import FastAPI
from app.routes import user_routes


app = FastAPI(
    title="IAM Application"
)


app.include_router(user_routes.router)


@app.get("/")
def root():
    return {
        "message": "IAM Application Running"
    }