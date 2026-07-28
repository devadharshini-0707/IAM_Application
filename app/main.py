from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth_routes
from app.routes import user_routes

app = FastAPI(
    title="IAM Application",
    debug=True,
)
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.config.settings import get_settings

settings = get_settings()

print("=" * 60)
print("SECRET_KEY:", settings.secret_key)
print("DATABASE_URL:", settings.database_url)
print("JWT_ALGORITHM:", settings.jwt_algorithm)
print("=" * 60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5178",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(ConflictError)
async def conflict_exception_handler(
    request: Request,
    exc: ConflictError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

app.include_router(user_routes.router)
app.include_router(auth_routes.router)


@app.get("/")
def root():
    return {
        "message": "IAM Application Running",
    }