import yaml
import os
from pydantic import BaseModel
from typing import Dict, Any, Optional

class ServiceConfig(BaseModel):
    enabled: bool = False
    api_key: Optional[str] = None
    url: Optional[str] = None

class NexusConfig(BaseModel):
    services: Dict[str, ServiceConfig] = {}

class Settings:
    def __init__(self, config_path: str = "/config/nexus/nexus.yml"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> NexusConfig:
        if not os.path.exists(self.config_path):
            return NexusConfig()
        
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
                return NexusConfig(**data)
        except Exception:
            return NexusConfig()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config.dict(), f)

settings = Settings()
