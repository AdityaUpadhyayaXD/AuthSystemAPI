from fastapi import FastAPI
from app.api.users import router as users_router
from app.database import Base
from app.database import engine
from app.api.auth import router as auth_router
from app.models.user import User
from app.models.refresh_token import RefreshToken

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication API",
    version="1.0.0"
)

# Register routes
app.include_router(auth_router)
app.include_router(users_router)
@app.get("/")
def root():
    return {
        "message": "Authentication API Running"
    }