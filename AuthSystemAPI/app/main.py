from fastapi import FastAPI

from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "AuthSystem API Running"
    }