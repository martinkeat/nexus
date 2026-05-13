import aiohttp
from .base import ServiceAdapter, HealthStatus
from typing import Dict, List, Optional, Any

class FlareSolverrAdapter(ServiceAdapter):
    def __init__(self, internal_url: str = "http://127.0.0.1:8191"):
        super().__init__("flaresolverr", internal_url)

    async def health_check(self) -> HealthStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.internal_url, timeout=2) as resp:
                    # FlareSolverr returns version info on root
                    if resp.status == 200:
                        return HealthStatus.HEALTHY
                    return HealthStatus.ERROR
        except Exception:
            return HealthStatus.STOPPED

    async def version(self) -> Optional[str]:
        return "FlareSolverr version placeholder"

    async def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "health": await self.health_check()
        }

    async def collect_logs(self, lines: int = 100) -> List[str]:
        return ["FlareSolverr logs placeholder"]
