from fastapi import FastAPI

app = FastAPI()
from app.routes import user_routes

app.include_router(user_routes.router)

# app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Hello"}