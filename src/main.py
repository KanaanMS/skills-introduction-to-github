"""FastAPI entrypoint that exposes both the vision and language services."""

from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.models.schemas import (
    HealthStatus,
    LLMRequest,
    LLMResponse,
    VisionPredictionResponse,
)
from src.services.llm import LLMService, LLMServiceError
from src.services.vision import VisionService, VisionServiceError

app = FastAPI(
    title="Cloud AI SaaS",
    version="0.1.0",
    description=(
        "Reference implementation of the 5CCSACCA coursework. "
        "The API bundles a computer vision service backed by Ultralytics YOLO and "
        "a natural language service backed by BitNet."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vision_service = VisionService()
llm_service = LLMService()


@app.get("/health", response_model=HealthStatus)
async def health() -> HealthStatus:
    """Expose the current backend configuration for quick diagnostics."""

    return HealthStatus(
        api="ok",
        vision_backend=vision_service.backend_name,
        llm_backend=llm_service.backend_name,
    )


@app.post("/vision/predict", response_model=VisionPredictionResponse)
async def predict_image(file: UploadFile = File(...)) -> VisionPredictionResponse:
    """Perform object detection on the uploaded image."""

    try:
        image_bytes = await file.read()
        return vision_service.predict(image_bytes)
    except VisionServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/llm/generate", response_model=LLMResponse)
async def generate_text(payload: LLMRequest) -> LLMResponse:
    """Generate text using the BitNet language model (or a deterministic fallback)."""

    try:
        return llm_service.generate(payload.prompt)
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/")
async def root() -> dict[str, str]:
    """Provide a friendly welcome message for quick smoke testing."""

    return {
        "message": "Welcome to the Cloud AI SaaS reference implementation.",
        "docs_url": "/docs",
    }

