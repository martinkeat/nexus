from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    STARTING = "starting"
    STOPPED = "stopped"
    DISABLED = "disabled"
    WARNING = "warning"
    ERROR = "error"
    UNCONFIGURED = "unconfigured"

class ServiceAdapter(ABC):
    def __init__(self, name: str, internal_url: str):
        self.name = name
        self.internal_url = internal_url

    @abstractmethod
    async def health_check(self) -> HealthStatus:
        pass

    @abstractmethod
    async def version(self) -> Optional[str]:
        pass

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def collect_logs(self, lines: int = 100) -> List[str]:
        pass
