from fastapi import FastAPI
import uvicorn
import os
from adapters.qbittorrent import QBittorrentAdapter
from adapters.sabnzbd import SABnzbdAdapter
from adapters.arr import SonarrAdapter, RadarrAdapter, LidarrAdapter, WhisparrAdapter, ProwlarrAdapter
from adapters.overseerr import OverseerrAdapter
from adapters.flaresolverr import FlareSolverrAdapter
from adapters.transcoder import TranscoderAdapter

app = FastAPI(title="Nexus API", version="0.1.0")

# Service Registry
adapters = {
    "qbittorrent": QBittorrentAdapter(),
    "sabnzbd": SABnzbdAdapter(),
    "sonarr": SonarrAdapter(),
    "radarr": RadarrAdapter(),
    "lidarr": LidarrAdapter(),
    "whisparr": WhisparrAdapter(),
    "prowlarr": ProwlarrAdapter(),
    "overseerr": OverseerrAdapter(),
    "flaresolverr": FlareSolverrAdapter(),
    "transcoder": TranscoderAdapter()
}

@app.post("/api/services/{service_name}/restart")
async def restart_service(service_name: str):
    if service_name not in adapters:
        return {"error": "Service not found"}, 404
    # TODO: Implement s6-overlay restart via adapter
    return {"message": f"Restart request sent for {service_name}"}

@app.get("/api/settings")
async def get_settings():
    from core.settings import settings
    return settings.config.dict()

@app.put("/api/settings")
async def update_settings(new_settings: dict):
    from core.settings import settings
    # TODO: Validate and update settings
    return {"message": "Settings updated"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "nexus-api"}

@app.get("/api/status")
async def status():
    service_status = {}
    for name, adapter in adapters.items():
        service_status[name] = await adapter.get_status()
    
    return {
        "nexus": "healthy",
        "services": service_status
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
