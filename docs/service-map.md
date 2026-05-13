# Nexus Service Map

## Service Registry

Each service in Nexus is managed through a typed adapter and controlled by the process supervisor. Services can be individually enabled or disabled.

## Service Definitions

| Service        | Binary/Process     | Internal Bind         | Default State | Toggleable |
|----------------|--------------------|-----------------------|---------------|------------|
| nexus-api      | python (FastAPI)   | 0.0.0.0:8080          | Always on     | No         |
| nexus-web      | (served by API)    | (same as API)         | Always on     | No         |
| nexus-worker   | python (asyncio)   | N/A (no port)         | Always on     | No         |
| nexus-transcoder| python + ffmpeg   | N/A (no port)         | Configurable  | Yes        |
| qbittorrent-nox| qbittorrent-nox    | 127.0.0.1:8091        | Configurable  | Yes        |
| SABnzbd        | sabnzbd            | 127.0.0.1:8092        | Configurable  | Yes        |
| Sonarr         | Sonarr             | 127.0.0.1:8989        | Configurable  | Yes        |
| Radarr         | Radarr             | 127.0.0.1:7878        | Configurable  | Yes        |
| Lidarr         | Lidarr             | 127.0.0.1:8686        | Configurable  | Yes        |
| Whisparr       | Whisparr           | 127.0.0.1:6969        | Configurable  | Yes        |
| Prowlarr       | Prowlarr           | 127.0.0.1:9696        | Configurable  | Yes        |
| Overseerr      | Overseerr          | 127.0.0.1:5055        | Configurable  | Yes        |
| FlareSolverr   | FlareSolverr       | 127.0.0.1:8191        | Configurable  | Yes        |

## External Ports

Only these ports are exposed from the container:

| Port       | Protocol | Purpose                |
|------------|----------|------------------------|
| 8080       | TCP      | Nexus GUI and API      |
| 6881       | TCP      | BitTorrent incoming    |
| 6881       | UDP      | BitTorrent incoming    |

All native service UIs are bound to `127.0.0.1` and are **not** reachable from outside the container.

A debug mode may be added later to optionally expose native UIs, but this must be explicitly enabled by the user and is disabled by default.

## Service Dependencies

```
nexus-api (always)
├── nexus-worker (always)
│   ├── nexus-transcoder (if transcoding enabled)
│   └── ffmpeg/ffprobe (if transcoding enabled)
├── qbittorrent-nox (if torrents enabled)
├── SABnzbd (if usenet enabled)
├── Sonarr (if TV enabled)
├── Radarr (if movies enabled)
├── Lidarr (if music enabled)
├── Whisparr (if adult enabled)
├── Prowlarr (if any Arr app enabled)
├── Overseerr (if requests enabled)
└── FlareSolverr (if configured for Prowlarr)
```

## Service Interconnections

```
Prowlarr ──→ Sonarr
Prowlarr ──→ Radarr
Prowlarr ──→ Lidarr
Prowlarr ──→ Whisparr

Sonarr   ──→ qBittorrent and/or SABnzbd
Radarr   ──→ qBittorrent and/or SABnzbd
Lidarr   ──→ qBittorrent and/or SABnzbd
Whisparr ──→ qBittorrent and/or SABnzbd

Overseerr ──→ Sonarr
Overseerr ──→ Radarr

FlareSolverr ──→ Prowlarr (where needed for indexer access)
```

## Health State Model

Each service adapter reports one of these normalised states:

| State          | Meaning                                              |
|----------------|------------------------------------------------------|
| `healthy`      | Service is running and responding to API calls        |
| `starting`     | Service process exists but API is not yet responsive  |
| `stopped`      | Service is toggled on but process is not running      |
| `disabled`     | Service is toggled off by user                        |
| `warning`      | Service is running but reports degraded state         |
| `error`        | Service is running but API calls are failing          |
| `unconfigured` | Service is enabled but has not completed first setup  |

## Adapter Interface

Every service adapter implements this interface:

```python
class ServiceAdapter:
    async def health_check(self) -> HealthStatus
    async def version(self) -> str | None
    async def read_config(self) -> dict
    async def write_config(self, config: dict) -> bool
    async def is_enabled(self) -> bool
    async def set_enabled(self, enabled: bool) -> None
    async def restart(self) -> bool
    async def status(self) -> ServiceStatus
    async def test_connectivity(self) -> ConnectivityResult
    async def collect_logs(self, lines: int = 100) -> list[str]
    async def report_errors(self) -> list[ServiceError]
```

## Process Supervisor Integration

s6-overlay manages each service as a `longrun` service type:

- Each service has a `run` script in `/etc/s6-overlay/s6-rc.d/`
- Each service has a `finish` script for clean shutdown
- Service dependencies are declared via s6's dependency system
- The Nexus worker communicates with s6 to start/stop toggled services
- Nexus reads s6 service state to supplement adapter health checks
