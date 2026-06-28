import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")


@dataclass
class AgentConfig:
    model_backend: str = os.getenv("MODEL_BACKEND", "gemini")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/google/gemma-2-9b-it:free")
    mcp_server_port: int = 8090
    max_iterations: int = 50
    pii_redaction_enabled: bool = True
    injection_detection_enabled: bool = True


config = AgentConfig()
