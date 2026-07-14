"""Calibration notes for optional LLM judges."""

CALIBRATION_NOTES = [
    "Use a fixed rubric and structured output schema.",
    "Compare judge scores with human-reviewed examples before relying on results.",
    "Check repeated runs for consistency if the provider is non-deterministic.",
    "Track model version, prompt version, cost and failure cases.",
    "Do not use judge scores as the only approval signal for high-risk outputs.",
]
