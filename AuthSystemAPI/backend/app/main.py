from fastapi import FastAPI

app = FastAPI(
    title="Authentication API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Authentication API is running"
    }