# Nexus

**A unified media automation platform in a single Docker container.**

Nexus consolidates qBittorrent, SABnzbd, Sonarr, Radarr, Lidarr, Whisparr, Prowlarr, Overseerr, FlareSolverr, and FFmpeg-based transcoding behind one beautiful, modern web interface.

## Features

- **One container** — All services managed by a single process supervisor
- **One login** — Unified authentication across all services
- **One dashboard** — Overview of downloads, media, health, and activity
- **Service toggles** — Enable only the services you need
- **Download flexibility** — Torrents, Usenet, or both with preference and fallback options
- **Nexus Regulariser** — FFmpeg-based transcoding with per-library profiles
- **GPU acceleration** — Auto-detection for NVIDIA, Intel, and AMD hardware encoding
- **Dark-first design** — Built on Tabler for a premium, responsive experience
- **Unraid-ready** — Designed for Unraid with safe, non-invasive deployment

## Quick Start

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
  ghcr.io/martinkeat/nexus:latest
```

Then open `http://<your-server>:8080` and complete the first-run wizard.

## Documentation

- [Architecture](docs/architecture.md)
- [Service Map](docs/service-map.md)
- [Folder Map](docs/folder-map.md)
- [Security Boundaries](docs/security-boundaries.md)
- [Unraid Deployment](docs/unraid-deployment.md)
- [Transcoding](docs/transcoding.md)
- [GPU Passthrough](docs/gpu-passthrough.md)
- [Settings Registry](docs/settings-registry.md)
- [Test Strategy](docs/test-strategy.md)
- [Release Process](docs/release-process.md)

## Status

🚧 **Under active development** — Not yet ready for production use.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

Created by [spontaneocus](https://github.com/martinkeat)
