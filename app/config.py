from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    host: str = "0.0.0.0"
    port: int = 8080


def load_config() -> Config:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    return Config(host=host, port=port)

