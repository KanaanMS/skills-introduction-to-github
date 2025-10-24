"""Utilities for running computer vision inference with Ultralytics YOLO."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List

import numpy as np
from PIL import Image

from src.models.schemas import Detection, VisionPredictionResponse

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - handled gracefully via fallback logic
    YOLO = None  # type: ignore[assignment]


class VisionServiceError(RuntimeError):
    """Raised when the YOLO backend is not available or a prediction fails."""


@dataclass
class _YOLOBox:
    """Internal representation of a YOLO prediction."""

    xmin: float
    ymin: float
    xmax: float
    ymax: float
    confidence: float
    class_id: int
    class_name: str | None

    def to_detection(self) -> Detection:
        return Detection(
            xmin=self.xmin,
            ymin=self.ymin,
            xmax=self.xmax,
            ymax=self.ymax,
            confidence=self.confidence,
            class_id=self.class_id,
            class_name=self.class_name,
        )


class VisionService:
    """Lightweight service that wraps Ultralytics YOLO inference."""

    def __init__(self, model_path: str = "yolo11n.pt", enable_mock: bool = True) -> None:
        self.model_path = model_path
        self.enable_mock = enable_mock
        self._model = None

    @property
    def backend_name(self) -> str:
        if self._model is not None:
            return "ultralytics-yolo"
        if YOLO is None:
            return "mock"
        return "ultralytics-yolo"

    def load_model(self) -> None:
        if self._model is not None:
            return
        if YOLO is None:
            raise VisionServiceError(
                "Ultralytics is not installed. Install it or enable the mock backend."
            )
        try:
            self._model = YOLO(self.model_path)
        except Exception as exc:  # pragma: no cover - depends on external weights
            raise VisionServiceError(f"Failed to load YOLO model: {exc}") from exc

    def _extract_boxes(self, results) -> List[_YOLOBox]:  # pragma: no cover - depends on YOLO internals
        boxes: List[_YOLOBox] = []
        if not results:
            return boxes
        names: Dict[int, str] = getattr(getattr(self._model, "model", self._model), "names", {}) or {}
        for result in results:
            if not hasattr(result, "boxes") or result.boxes is None:
                continue
            raw_boxes = result.boxes
            xyxy = raw_boxes.xyxy.cpu().numpy()
            confidences = raw_boxes.conf.cpu().numpy() if raw_boxes.conf is not None else np.zeros(len(xyxy))
            class_ids = raw_boxes.cls.cpu().numpy() if raw_boxes.cls is not None else np.zeros(len(xyxy))
            for idx, coords in enumerate(xyxy):
                xmin, ymin, xmax, ymax = coords.tolist()
                confidence = float(confidences[idx]) if idx < len(confidences) else 0.0
                class_id = int(class_ids[idx]) if idx < len(class_ids) else 0
                boxes.append(
                    _YOLOBox(
                        xmin=float(xmin),
                        ymin=float(ymin),
                        xmax=float(xmax),
                        ymax=float(ymax),
                        confidence=float(confidence),
                        class_id=class_id,
                        class_name=names.get(class_id),
                    )
                )
        return boxes

    def predict(self, image_bytes: bytes) -> VisionPredictionResponse:
        if not image_bytes:
            raise VisionServiceError("Empty payload received; supply an image to perform inference.")

        if YOLO is None:
            if self.enable_mock:
                return VisionPredictionResponse(
                    detections=[],
                    backend="mock",
                    detail="Ultralytics YOLO is unavailable; returning an empty set of detections.",
                )
            raise VisionServiceError("Ultralytics YOLO is unavailable and mocking is disabled.")

        self.load_model()

        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except Exception as exc:
            raise VisionServiceError(f"Failed to parse the provided image: {exc}") from exc

        np_image = np.array(image)
        try:
            results = self._model.predict(np_image, verbose=False)
        except Exception as exc:  # pragma: no cover - depends on external runtime
            raise VisionServiceError(f"YOLO prediction failed: {exc}") from exc

        detections = [box.to_detection() for box in self._extract_boxes(results)]
        return VisionPredictionResponse(detections=detections, backend="ultralytics-yolo")

