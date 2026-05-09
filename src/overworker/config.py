from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("OVERWORKER_ENV", "development")
    output_dir: str = os.getenv("OVERWORKER_OUTPUT_DIR", "./out")
    max_file_bytes: int = int(os.getenv("OVERWORKER_MAX_FILE_BYTES", "200000"))
    enable_network: bool = os.getenv("OVERWORKER_ENABLE_NETWORK", "false").lower() == "true"
    enable_shell: bool = os.getenv("OVERWORKER_ENABLE_SHELL", "false").lower() == "true"
    llm_provider: str = os.getenv("OVERWORKER_LLM_PROVIDER", "none")
    llm_model: str = os.getenv("OVERWORKER_LLM_MODEL", "")


settings = Settings()
