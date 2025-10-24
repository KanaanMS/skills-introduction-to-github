"""Wrapper around BitNet language model interactions."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from src.models.schemas import LLMResponse

try:
    from bitnet import BitNet
except Exception:  # pragma: no cover - depends on optional dependency
    BitNet = None  # type: ignore[assignment]


class LLMServiceError(RuntimeError):
    """Raised when the BitNet backend is unavailable or rejects an input."""


@dataclass
class LLMService:
    """Service responsible for communicating with BitNet or a lightweight fallback."""

    model_name: str = "bitnet/BitNet-1.58B"
    temperature: float = 0.7
    enable_mock: bool = True

    def __post_init__(self) -> None:
        self._model = None
        if BitNet is not None:
            try:  # pragma: no cover - requires external weights
                self._model = BitNet.from_pretrained(self.model_name)
            except Exception as exc:  # pragma: no cover - depends on runtime
                if not self.enable_mock:
                    raise LLMServiceError(f"Failed to initialise BitNet: {exc}") from exc

    @property
    def backend_name(self) -> str:
        if self._model is not None:
            return "bitnet"
        if BitNet is None:
            return "mock"
        return "mock"

    def _mock_generate(self, prompt: str) -> str:
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]
        return (
            "BitNet placeholder response. Install the official model to replace this message. "
            f"Prompt digest: {digest}."
        )

    def generate(self, prompt: str) -> LLMResponse:
        if not prompt or not prompt.strip():
            raise LLMServiceError("Prompt cannot be empty.")

        if self._model is None:
            if not self.enable_mock:
                raise LLMServiceError("BitNet model is unavailable and mocking is disabled.")
            return LLMResponse(
                response=self._mock_generate(prompt.strip()),
                backend="mock",
                detail="BitNet Python package not installed; using deterministic mock response.",
            )

        try:  # pragma: no cover - requires actual BitNet weights
            generated = self._model.generate(prompt, temperature=self.temperature)
        except Exception as exc:  # pragma: no cover - depends on runtime
            raise LLMServiceError(f"BitNet generation failed: {exc}") from exc

        return LLMResponse(response=str(generated), backend="bitnet")

