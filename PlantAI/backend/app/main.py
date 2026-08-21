from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.routes.prediction import router as prediction_router

app = FastAPI(
    title="PlantAI",
    description="AI Plant Disease Detection System",
    version="1.0.0"
)

# Serve CSS, JS, images, etc.
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

# API routes
app.include_router(prediction_router)


# Home page
@app.get("/")
async def home():
    return FileResponse("frontend/index.html")


# Result page
@app.get("/result.html")
async def result_page():
    return FileResponse("frontend/result.html")


# History page
@app.get("/history.html")
async def history_page():
    return FileResponse("frontend/history.html")


# Health check
@app.get("/health")
async def health():
    return {
        "status": "running",
        "message": "PlantAI Backend is running"
    }