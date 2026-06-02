from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Software Engineering Team"
    }

@app.get("/health")
def health():
    return {
        "status": "running"
    }