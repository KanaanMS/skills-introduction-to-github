"""Pydantic schemas shared by the FastAPI application."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Detection(BaseModel):
    """Single detection prediction from the vision service."""

    xmin: float = Field(..., description="Left coordinate of the bounding box in pixels.")
    ymin: float = Field(..., description="Top coordinate of the bounding box in pixels.")
    xmax: float = Field(..., description="Right coordinate of the bounding box in pixels.")
    ymax: float = Field(..., description="Bottom coordinate of the bounding box in pixels.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score provided by the model.")
    class_id: int = Field(..., ge=0, description="Numeric class identifier assigned by YOLO.")
    class_name: Optional[str] = Field(None, description="Human readable label for the detected class, when available.")


class VisionPredictionResponse(BaseModel):
    """Response body returned by the vision inference endpoint."""

    detections: List[Detection] = Field(default_factory=list, description="List of model detections.")
    backend: str = Field(..., description="Name of the underlying inference backend.")
    detail: Optional[str] = Field(
        None,
        description="Optional detail or warning when running in a degraded mode.",
    )


class LLMRequest(BaseModel):
    """Request body accepted by the BitNet-backed endpoint."""

    prompt: str = Field(..., min_length=1, description="Prompt to send to the language model.")


class LLMResponse(BaseModel):
    """Response body produced by the language model service."""

    response: str = Field(..., description="Generated text returned by the model or fallback implementation.")
    backend: str = Field(..., description="Identifier of the backend used to create the response.")
    detail: Optional[str] = Field(
        None,
        description="Optional context about the backend execution.",
    )


class HealthStatus(BaseModel):
    """Simple schema for the `/health` endpoint."""

    api: str = Field(..., description="General availability of the FastAPI service.")
    vision_backend: str = Field(..., description="Name of the configured computer vision backend.")
    llm_backend: str = Field(..., description="Name of the configured language model backend.")

