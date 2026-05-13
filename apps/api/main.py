from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Nexus API", version="0.1.0")

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "nexus-api"}

@app.get("/api/status")
async def status():
    return {
        "nexus": "starting",
        "services": {
            "sonarr": "unconfigured",
            "radarr": "unconfigured",
            "qbittorrent": "unconfigured"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
