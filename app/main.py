from fastapi import FastAPI

app = FastAPI(
    title="AI Fabric",
    description="An intelligent AI gateway for reliable model access.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-fabric",
    }
