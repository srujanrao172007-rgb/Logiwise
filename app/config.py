import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")


@dataclass
class AgentConfig:
    model_backend: str = os.getenv("MODEL_BACKEND", "nvidia")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/nvidia/nemotron-3-super-120b-a12b:free")
    nvidia_model: str = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-4-340b-instruct")
    nvidia_api_key: str = os.getenv("NVIDIA_API_KEY", "")
    max_iterations: int = 50
    pii_redaction_enabled: bool = True
    injection_detection_enabled: bool = True


config = AgentConfig()
