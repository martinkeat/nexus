from fastapi import FastAPI
import uvicorn
import os
from adapters.qbittorrent import QBittorrentAdapter
from adapters.sabnzbd import SABnzbdAdapter

app = FastAPI(title="Nexus API", version="0.1.0")

# Service Registry
adapters = {
    "qbittorrent": QBittorrentAdapter(),
    "sabnzbd": SABnzbdAdapter()
}

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
