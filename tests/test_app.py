from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from src.main import app


def _make_image_bytes() -> bytes:
    image = Image.new("RGB", (4, 4), color=(255, 0, 0))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_health_endpoint_exposes_backends():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["api"] == "ok"
    assert "backend" in payload["vision_backend"] or payload["vision_backend"] in {"mock", "ultralytics-yolo"}
    assert payload["llm_backend"] in {"mock", "bitnet"}


def test_llm_generate_returns_response():
    client = TestClient(app)
    response = client.post("/llm/generate", json={"prompt": "Hello there"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["response"]
    assert payload["backend"] in {"mock", "bitnet"}


def test_vision_endpoint_accepts_image():
    client = TestClient(app)
    files = {"file": ("red.png", _make_image_bytes(), "image/png")}
    response = client.post("/vision/predict", files=files)
    assert response.status_code == 200
    payload = response.json()
    assert "detections" in payload
    assert payload["backend"] in {"mock", "ultralytics-yolo"}

