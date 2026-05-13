import aiohttp
from .base import ServiceAdapter, HealthStatus
from typing import Dict, List, Optional, Any

class OverseerrAdapter(ServiceAdapter):
    def __init__(self, internal_url: str = "http://127.0.0.1:5055"):
        super().__init__("overseerr", internal_url)
        self.api_key: Optional[str] = None

    async def health_check(self) -> HealthStatus:
        if not self.api_key:
            return HealthStatus.UNCONFIGURED
            
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"X-Api-Key": self.api_key}
                async with session.get(f"{self.internal_url}/api/v1/status", headers=headers, timeout=2) as resp:
                    if resp.status == 200:
                        return HealthStatus.HEALTHY
                    return HealthStatus.ERROR
        except Exception:
            return HealthStatus.STOPPED

    async def version(self) -> Optional[str]:
        return "Overseerr version placeholder"

    async def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "health": await self.health_check()
        }

    async def collect_logs(self, lines: int = 100) -> List[str]:
        return ["Overseerr logs placeholder"]
