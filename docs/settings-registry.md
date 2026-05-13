# Nexus Settings Registry

## Overview

Nexus centralises all user-facing configuration into a typed settings registry. Settings are persisted in `/config/nexus/nexus.db` (SQLite) and exposed through the Nexus API and Settings UI.

## Settings Categories

### General

| Key                        | Type    | Default          | Description                        |
|----------------------------|---------|------------------|------------------------------------|
| `general.instance_name`    | string  | `"Nexus"`        | Display name for this instance     |
| `general.base_url`         | string  | `"/"`            | Base URL path for reverse proxy    |
| `general.timezone`         | string  | `"Etc/UTC"`      | Timezone for display and scheduling|
| `general.log_level`        | enum    | `"info"`         | Logging verbosity                  |

### Authentication

| Key                        | Type    | Default          | Description                        |
|----------------------------|---------|------------------|------------------------------------|
| `auth.session_timeout`     | integer | `86400`          | Session duration in seconds        |
| `auth.trusted_proxies`     | list    | `[]`             | Trusted reverse proxy IP ranges    |
| `auth.api_tokens`          | list    | `[]`             | Managed API bearer tokens          |

### Services

Each service has a toggle and basic connection settings:

| Key                              | Type    | Default | Description                    |
|----------------------------------|---------|---------|--------------------------------|
| `services.sonarr.enabled`        | boolean | `true`  | Enable Sonarr                  |
| `services.radarr.enabled`        | boolean | `true`  | Enable Radarr                  |
| `services.lidarr.enabled`        | boolean | `true`  | Enable Lidarr                  |
| `services.whisparr.enabled`      | boolean | `false` | Enable Whisparr                |
| `services.prowlarr.enabled`      | boolean | `true`  | Enable Prowlarr                |
| `services.overseerr.enabled`     | boolean | `true`  | Enable Overseerr               |
| `services.flaresolverr.enabled`  | boolean | `false` | Enable FlareSolverr            |
| `services.qbittorrent.enabled`   | boolean | `true`  | Enable qBittorrent             |
| `services.sabnzbd.enabled`       | boolean | `false` | Enable SABnzbd                 |
| `services.transcoding.enabled`   | boolean | `false` | Enable Nexus Regulariser       |

### Download Sources

| Key                              | Type    | Default          | Description                    |
|----------------------------------|---------|------------------|--------------------------------|
| `downloads.mode`                 | enum    | `"torrents"`     | torrents / usenet / both       |
| `downloads.preference`           | enum    | `"none"`         | prefer_usenet / prefer_torrent / none |
| `downloads.fallback`             | boolean | `false`          | Fallback to other source on failure |

### Transcoding Profiles

Stored as structured objects per library type. See [transcoding.md](transcoding.md) for full profile schema.

### GPU

| Key                              | Type    | Default          | Description                    |
|----------------------------------|---------|------------------|--------------------------------|
| `gpu.mode`                       | enum    | `"auto"`         | auto / nvidia / intel / amd / cpu / disabled |
| `gpu.detected_vendor`            | string  | `null`           | Last detected GPU vendor       |
| `gpu.detected_encoders`          | list    | `[]`             | Last detected encoder list     |
| `gpu.last_detection`             | datetime| `null`           | Timestamp of last detection    |

## Settings Persistence

- All settings are stored in SQLite at `/config/nexus/nexus.db`
- Settings are read into memory on startup
- Changes are written immediately to disk
- A settings change triggers relevant service restarts or adapter reconfiguration
- Settings schema is versioned; migrations are applied automatically on upgrade

## Settings API

```
GET    /api/settings                    # Get all settings
GET    /api/settings/{category}         # Get settings by category
PUT    /api/settings/{category}         # Update settings in a category
POST   /api/settings/reset/{category}   # Reset category to defaults
GET    /api/settings/schema             # Get settings schema with types/defaults
```

## Validation

- All settings are validated against their schema before persistence
- Invalid values are rejected with descriptive error messages
- Enum values are checked against allowed lists
- Dependent settings are cross-validated (e.g., GPU mode vs. detected capabilities)
