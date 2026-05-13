# Nexus Folder Map

## Host Volume Mounts

The user maps these host paths into the container:

| Container Path | Purpose                                    | Required |
|----------------|--------------------------------------------|----------|
| `/config`      | All Nexus and service configuration         | Yes      |
| `/downloads`   | Download staging (incomplete + complete)    | Yes      |
| `/tv`          | Sonarr final library                        | If Sonarr enabled  |
| `/movies`      | Radarr final library                        | If Radarr enabled  |
| `/music`       | Lidarr final library                        | If Lidarr enabled  |
| `/adult`       | Whisparr final library                      | If Whisparr enabled|
| `/transcode`   | FFmpeg work queue, logs, temporary files    | If transcoding enabled |

## Internal Directory Structure

### /config

```
/config
├── nexus/
│   ├── nexus.db              # SQLite database
│   ├── nexus.yml             # Primary configuration
│   ├── secrets.yml           # Internal API keys (encrypted, never committed)
│   └── backups/              # Automatic config backups
├── qbittorrent/
│   ├── qBittorrent/
│   │   └── config/
│   │       └── qBittorrent.conf
│   └── BT_backup/
├── sabnzbd/
│   └── sabnzbd.ini
├── sonarr/
│   ├── config.xml
│   └── logs/
├── radarr/
│   ├── config.xml
│   └── logs/
├── lidarr/
│   ├── config.xml
│   └── logs/
├── whisparr/
│   ├── config.xml
│   └── logs/
├── prowlarr/
│   ├── config.xml
│   └── logs/
├── overseerr/
│   └── settings.json
├── flaresolverr/
│   └── (runtime state only)
└── ffmpeg/
    ├── profiles/             # User-defined transcoding profiles
    └── presets/              # Built-in transcoding presets
```

### /downloads

```
/downloads
├── incomplete/
│   ├── torrents/             # qBittorrent active downloads
│   └── usenet/               # SABnzbd active downloads
└── complete/
    ├── torrents/
    │   ├── tv/               # Completed torrent TV downloads
    │   ├── movies/           # Completed torrent movie downloads
    │   ├── music/            # Completed torrent music downloads
    │   └── adult/            # Completed torrent adult downloads
    └── usenet/
        ├── tv/               # Completed usenet TV downloads
        ├── movies/           # Completed usenet movie downloads
        ├── music/            # Completed usenet music downloads
        └── adult/            # Completed usenet adult downloads
```

### /transcode

```
/transcode
├── queue/                    # Files waiting for transcoding
├── working/                  # Currently being transcoded
├── completed/                # Transcoded output awaiting import
├── failed/                   # Failed transcode attempts (for review)
└── logs/                     # Per-file FFmpeg logs
```

### Library paths

```
/tv                           # Sonarr-managed TV library
/movies                       # Radarr-managed movie library
/music                        # Lidarr-managed music library
/adult                        # Whisparr-managed adult library
```

## Folder Creation Policy

- **Container startup**: Nexus creates all subdirectories under `/config`, `/downloads`, and `/transcode` if they do not exist.
- **Library paths** (`/tv`, `/movies`, `/music`, `/adult`): Nexus verifies they are mounted and writable but does **not** create them. If missing, report clearly in the dashboard and first-run wizard.
- **Host-level shares**: Nexus never creates or modifies host-level shares, Unraid shares, or mount points.

## Permission Model

- Nexus runs internal processes with a configurable PUID/PGID (default: 99/100 for Unraid `nobody:users`).
- All file operations respect the configured UID/GID.
- On startup, Nexus performs permission checks on all mounted paths and reports failures.
- Nexus does **not** run `chmod` or `chown` on broad host paths. If permissions are wrong, it reports the exact path, expected UID/GID, and remediation instructions.
