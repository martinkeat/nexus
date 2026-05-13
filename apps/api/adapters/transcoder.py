import subprocess
import json
from .base import ServiceAdapter, HealthStatus
from typing import Dict, List, Optional, Any

class TranscoderAdapter(ServiceAdapter):
    def __init__(self):
        super().__init__("transcoder", "internal")

    async def health_check(self) -> HealthStatus:
        try:
            # Check if ffmpeg and ffprobe are available in the path
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            subprocess.run(["ffprobe", "-version"], capture_output=True, check=True)
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.ERROR

    async def version(self) -> Optional[str]:
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            return result.stdout.split('\n')[0]
        except Exception:
            return None

    async def probe_file(self, file_path: str) -> Dict[str, Any]:
        try:
            cmd = [
                "ffprobe", 
                "-v", "quiet", 
                "-print_format", "json", 
                "-show_format", 
                "-show_streams", 
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}

    async def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": await self.version(),
            "health": await self.health_check(),
            "capabilities": await self.get_capabilities()
        }

    async def get_capabilities(self) -> Dict[str, Any]:
        # Placeholder for GPU detection
        return {
            "gpu": "none",
            "encoders": ["libx264", "libx265"]
        }

    async def collect_logs(self, lines: int = 100) -> List[str]:
        return ["Transcoding logs placeholder"]
