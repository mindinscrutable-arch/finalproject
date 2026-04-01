from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="LLM Migration Factory API",
    description="API for migrating workloads to Amazon Bedrock",
    version="1.0.0"
)

# Include central router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "LLM Migration Factory API is running"}
