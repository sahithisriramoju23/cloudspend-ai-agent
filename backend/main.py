"""
CloudSpend AI - Main Application Entry Point
"""
from fastapi import FastAPI

app = FastAPI(title="CloudSpend AI", version="1.0.0")

@app.get("/")
def root():
    return {"message": "CloudSpend AI Agent System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
