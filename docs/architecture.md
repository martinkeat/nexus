# Nexus Architecture

## Overview

Nexus is a single-container Docker application that provides a unified control plane for media automation. It consolidates multiple services behind one GUI, one login, and one management interface.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Nexus Container                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Process Supervisor (s6-overlay)         │    │
│  └──────────┬──────────────────────────────────────────────┘    │
│             │                                                   │
│  ┌──────────┴──────────────────────────────────────────────┐    │
│  │              Nexus Application Layer                     │    │
│  │                                                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │    │
│  │  │ nexus-api│  │ nexus-web│  │nexus-    │  │nexus-   │ │    │
│  │  │ (FastAPI)│  │ (Tabler) │  │worker    │  │transcdr │ │    │
│  │  │ :8080    │  │ (static) │  │(bg tasks)│  │(ffmpeg) │ │    │
│  │  └────┬─────┘  └──────────┘  └────┬─────┘  └────┬────┘ │    │
│  │       │                            │              │      │    │
│  │  ┌────┴────────────────────────────┴──────────────┴───┐  │    │
│  │  │              Service Adapter Layer                  │  │    │
│  │  │                                                     │  │    │
│  │  │  ┌─────────┐ ┌─────────┐ ┌────────┐ ┌───────────┐ │  │    │
│  │  │  │qBit     │ │SABnzbd  │ │Sonarr  │ │Radarr     │ │  │    │
│  │  │  │Adapter  │ │Adapter  │ │Adapter │ │Adapter    │ │  │    │
│  │  │  └────┬────┘ └────┬────┘ └───┬────┘ └─────┬─────┘ │  │    │
│  │  │  ┌────┴────┐ ┌────┴────┐ ┌───┴────┐ ┌─────┴─────┐ │  │    │
│  │  │  │Lidarr   │ │Whisparr │ │Prowlarr│ │Overseerr  │ │  │    │
│  │  │  │Adapter  │ │Adapter  │ │Adapter │ │Adapter    │ │  │    │
│  │  │  └─────────┘ └─────────┘ └────────┘ └───────────┘ │  │    │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │  │    │
│  │  │  │FlareSlvr │ │FFmpeg    │ │Runtime/Health    │   │  │    │
│  │  │  │Adapter   │ │Adapter   │ │Adapter           │   │  │    │
│  │  │  └──────────┘ └──────────┘ └──────────────────┘   │  │    │
│  │  └────────────────────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              Supervised Services                          │    │
│  │                                                           │    │
│  │  qbittorrent-nox  SABnzbd  Sonarr  Radarr  Lidarr       │    │
│  │  Whisparr  Prowlarr  Overseerr  FlareSolverr            │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              Shared Volumes                               │    │
│  │  /config  /downloads  /tv  /movies  /music  /adult       │    │
│  │  /transcode                                               │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer              | Technology               | Rationale                                      |
|--------------------|--------------------------|------------------------------------------------|
| Process supervisor | s6-overlay v3            | Proven in linuxserver.io containers, lightweight|
| API server         | Python 3.12 + FastAPI    | Async, typed, fast, excellent for adapters      |
| Web frontend       | Tabler (static build)    | Beautiful, responsive, dark-first design system |
| Background worker  | Python + asyncio         | Shares adapter code with API                    |
| Transcoder engine  | FFmpeg + ffprobe         | Industry standard, GPU-capable                  |
| Data store         | SQLite                   | Zero-dependency, file-based, /config-portable   |
| Configuration      | YAML + environment vars  | Human-readable, Docker-friendly                 |
| Base image         | Alpine Linux 3.20        | Small footprint, excellent package availability  |

## Design Principles

1. **Single container**: One image, one `docker run`, one management surface.
2. **Adapter pattern**: Every embedded service is accessed through a typed adapter that normalises health, config, and control operations.
3. **Service toggle**: Any embedded service can be enabled or disabled at runtime without breaking the system.
4. **No external exposure by default**: Native service UIs are bound to 127.0.0.1 and are not reachable from outside the container.
5. **Documentation-first**: No feature is implemented before its design is documented and reviewed.
6. **Test-driven safety**: Every feature has unit, integration, and container-level tests.
7. **Unraid-safe**: Nexus never modifies the host, never touches other containers, never alters shares or settings.

## Component Responsibilities

### nexus-api

- Serves the REST API at `:8080/api/`
- Serves the static Tabler web frontend at `:8080/`
- Manages authentication and sessions
- Routes requests to service adapters
- Provides WebSocket endpoints for real-time status

### nexus-web

- Static HTML/CSS/JS built from Tabler
- Communicates exclusively with `nexus-api`
- Dark-first, responsive, accessible
- No direct service communication

### nexus-worker

- Background task runner
- Monitors download completion events
- Triggers transcoding pipeline
- Runs periodic health checks
- Manages service lifecycle events

### nexus-transcoder

- FFmpeg/ffprobe wrapper
- Profile-based transcoding decisions
- GPU capability detection
- Queue management
- Output verification

## Data Flow

```
User Request → Overseerr → Sonarr/Radarr → Prowlarr → Indexers
                                    ↓
                        qBittorrent / SABnzbd
                                    ↓
                          /downloads/complete
                                    ↓
                    nexus-worker detects completion
                                    ↓
                  nexus-transcoder processes media
                                    ↓
                    Processed file → download folder
                                    ↓
                   Sonarr/Radarr imports to library
                                    ↓
                        /tv  /movies  /music  /adult
```

## State Management

All persistent state is stored under `/config`:

- `nexus/nexus.db` — SQLite database for Nexus settings, history, sessions
- `nexus/nexus.yml` — Primary Nexus configuration
- `nexus/secrets.yml` — Encrypted internal API keys (not committed, not logged)
- Service-specific directories contain each service's own configuration files

## Error Handling

- All adapter calls are wrapped in try/except with structured error responses
- Service failures are logged and surfaced in the dashboard as health status changes
- Transcoding failures are recorded with full ffmpeg output for debugging
- No silent swallowing of errors

## Upgrade Path

- Configuration is versioned with a schema version number
- On startup, Nexus checks schema version and runs migrations if needed
- Migrations are idempotent and logged
- Service configurations are preserved across upgrades
