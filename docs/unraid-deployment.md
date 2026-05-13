# Nexus Unraid Deployment Guide

## Overview

Nexus runs as a single Docker container on Unraid. It does not require Community Applications plugins, custom scripts, or host-level configuration changes.

## Prerequisites

- Unraid 6.12+ with Docker enabled
- At least one data share for media libraries
- Network access for downloading and indexer connectivity

## Volume Mappings

| Container Path | Host Path (example)                    | Purpose                        |
|----------------|----------------------------------------|--------------------------------|
| `/config`      | `/mnt/user/appdata/nexus`              | All configuration and state    |
| `/downloads`   | `/mnt/user/downloads`                  | Download staging               |
| `/tv`          | `/mnt/user/media_storage/sonarr`       | TV library                     |
| `/movies`      | `/mnt/user/media_storage/radarr`       | Movie library                  |
| `/music`       | `/mnt/user/media_storage/lidarr`       | Music library                  |
| `/adult`       | `/mnt/user/media_storage/whisparr`     | Adult library                  |
| `/transcode`   | `/mnt/user/appdata/nexus/transcode`    | Transcoding workspace          |

> **Note:** Adjust host paths to match your Unraid share layout. The container paths must remain exactly as shown.

## Port Mappings

| Container Port | Host Port | Protocol | Purpose              |
|----------------|-----------|----------|----------------------|
| 8080           | 8080      | TCP      | Nexus GUI and API    |
| 6881           | 6881      | TCP      | BitTorrent incoming  |
| 6881           | 6881      | UDP      | BitTorrent incoming  |

## Network Mode

**Recommended:** Bridge mode with the port mappings above.

**Alternative:** If using a macvlan/br0 network with a static IP, map all ports or use host networking for the container's dedicated IP.

## Environment Variables

| Variable | Default   | Purpose                          |
|----------|-----------|----------------------------------|
| `PUID`   | `99`      | Process user ID (Unraid nobody)  |
| `PGID`   | `100`     | Process group ID (Unraid users)  |
| `TZ`     | `Etc/UTC` | Timezone                         |
| `UMASK`  | `022`     | File creation mask               |

## GPU Passthrough (Optional)

### Intel / AMD (VAAPI)

Add device mapping:

```
/dev/dri:/dev/dri
```

### NVIDIA

Requires NVIDIA Container Runtime configured on the Unraid host. Add:

```
--runtime=nvidia
--gpus all
```

Or pass specific devices as required.

### No GPU

Nexus works without GPU passthrough. It will detect the absence and fall back to CPU-based transcoding (software encoding). The GPU capability panel will clearly show what is and is not available.

## Docker Run Example

```bash
docker run -d \
  --name nexus \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -e PUID=99 \
  -e PGID=100 \
  -e TZ=Europe/London \
  -v /mnt/user/appdata/nexus:/config \
  -v /mnt/user/downloads:/downloads \
  -v /mnt/user/media_storage/sonarr:/tv \
  -v /mnt/user/media_storage/radarr:/movies \
  -v /mnt/user/media_storage/lidarr:/music \
  -v /mnt/user/media_storage/whisparr:/adult \
  -v /mnt/user/appdata/nexus/transcode:/transcode \
  --device /dev/dri:/dev/dri \
  ghcr.io/martinkeat/nexus:latest
```

## Docker Compose Example

```yaml
services:
  nexus:
    image: ghcr.io/martinkeat/nexus:latest
    container_name: nexus
    ports:
      - "8080:8080"
      - "6881:6881"
      - "6881:6881/udp"
    environment:
      - PUID=99
      - PGID=100
      - TZ=Europe/London
    volumes:
      - /mnt/user/appdata/nexus:/config
      - /mnt/user/downloads:/downloads
      - /mnt/user/media_storage/sonarr:/tv
      - /mnt/user/media_storage/radarr:/movies
      - /mnt/user/media_storage/lidarr:/music
      - /mnt/user/media_storage/whisparr:/adult
      - /mnt/user/appdata/nexus/transcode:/transcode
    devices:
      - /dev/dri:/dev/dri
    restart: unless-stopped
```

## Safety Guarantees

- Nexus does **not** modify Unraid host settings
- Nexus does **not** modify other Docker containers
- Nexus does **not** modify Unraid shares, users, or permissions
- Nexus does **not** require privileged mode
- Nexus operates exclusively within its mapped volumes
- Removing the Nexus container and its `/config` volume cleanly removes all Nexus state

## First Run

1. Start the container
2. Navigate to `http://<server-ip>:8080`
3. Complete the first-run setup wizard
4. Nexus will guide you through service configuration

## Backup

All Nexus state is in `/config`. Back up this directory to preserve:

- Nexus settings and database
- All service configurations
- Transcoding profiles
- Internal API keys

## Upgrade

Pull the latest image and recreate the container. Configuration is preserved in `/config`.
